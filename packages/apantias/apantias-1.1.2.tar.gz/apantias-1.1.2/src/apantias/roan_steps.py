import gc
import os
import psutil
from datetime import datetime

import numpy as np

from . import logger
from . import utils
from . import analysis as an
from . import params
from . import fitting as fit
from . import file_io as io

"""
Planned structure of the analysis.h5 output file:
datasets: ~
groups: /
/offnoi
    /nrep_data
        ~signal_values
            # raw signals, averaged over nreps, after common mode correction
        ~slope_values
            # slope values (simple linear fit) of the raw signals
    /slopes
        /fit
            # slope values from precal are fitted pixel wise with a gaussian
            ~amplitude
            ~mean
            ~sigma
            ~error_amplitude
            ~error_mean
            ~error_sigma
        ~bad_slopes_mask
            # mask of bad slopes is calculated from the pixelwise fit and the threshold from the params file
        ~bad_slopes_count
            # count of number of bad slopes per pixel
        ~signal_values
            # raw signals after common mode correction, bad slopes are set to nan
    /outliers
        /fit
            # signal values after common mode correction and bad slopes removed are fitted pixel wise with a gaussian
            ~amplitude
            ~mean
            ~sigma
            ~error_amplitude
            ~error_mean
            ~error_sigma
        ~outliers_mask
            # mask of outliers is calculated from the pixelwise fit and the threshold from the params file
        ~outliers_count
            # count of number of outliers per pixel
    /fit
        # signal values after common mode correction, bad slopes removed and outliers removed are fitted pixel wise with a gaussian
        ~amplitude
        ~mean
        ~sigma
        ~error_amplitude
        ~error_mean
        ~error_sigma
    /final
        ~offset
            # offset value from the gaussian fit
        ~noise
            # noise value from the gaussian fit
        ~signal_values
            # raw signals after common mode correction, bad slopes removed, outliers removed and applied offset

/filter
    /nrep_data
        ~signal_values
            # raw signals, averaged over nreps, after common mode correction and offset from offnoi step subtracted
        ~slope_values
            # slope values (simple linear fit) of the raw signals
    /slopes
        /fit
            # slope values from precal are fitted pixel wise with a gaussian
            ~amplitude
            ~mean
            ~sigma
            ~error_amplitude
            ~error_mean
            ~error_sigma
        ~bad_slopes_mask
            # mask of bad slopes is calculated from the pixelwise fit and the threshold from the params file
        ~bad_slopes_count
            # count of number of bad slopes per pixel
        ~signal_values
            # raw signals after common mode correction, bad slopes are set to nan
    /outliers
        /fit
            # signal values after common mode correction and bad slopes removed are fitted pixel wise with a gaussian
            ~amplitude
            ~mean
            ~sigma
            ~error_amplitude
            ~error_mean
            ~error_sigma
        ~outliers_mask
            # mask of outliers is calculated from the pixelwise fit and the threshold from the params file
        ~outliers_count
            # count of number of outliers per pixel
    /events
        ~event_map
            # event map is calculated from the signal values, the noise values from the offnoi step and the thresholds from the params file
        ~event_map_counts
            # count of number of events per pixel
        ~event_details
            #TODO: implement pandas table with event details
        ~bleedthrough
            #TODO: implement bleedthrough calculation
/gain
    #TODO: Implement gain method
    /2_gauss_fit
        #TODO: Move simple 2 Gauss fit from filter step to here
    /signal_fit
        #TODO: somehow cut noise and fit a gaussian to the signal values

"""


class RoanSteps:
    _logger = logger.Logger("nproan-RoanSteps", "info").get_logger()

    def __init__(self, prm_file: str) -> None:
        self.load(prm_file)

    def load(self, prm_file: str) -> None:
        # load parameter file
        self.params = params.Params(prm_file)
        self.params_dict = self.params.get_dict()

        # polarity is from the old code, im not quite sure why it is -1
        self.polarity = -1

        # common parameters from params file
        self.results_dir = self.params_dict["common_results_dir"]
        self.ram_available = self.params_dict["common_available_ram"]

        # offnoi parameters from params file
        self.offnoi_data_file = self.params_dict["offnoi_data_file"]
        self.offnoi_nframes_eval = self.params_dict["offnoi_nframes_eval"]
        self.offnoi_nreps_eval = self.params_dict["offnoi_nreps_eval"]
        self.offnoi_comm_mode = self.params_dict["offnoi_comm_mode"]
        self.offnoi_thres_bad_slopes = self.params_dict["offnoi_thres_bad_slopes"]

        # filter parameters from params file
        self.filter_data_file = self.params_dict["filter_data_file"]
        self.filter_nframes_eval = self.params_dict["filter_nframes_eval"]
        self.filter_nreps_eval = self.params_dict["filter_nreps_eval"]
        self.filter_comm_mode = self.params_dict["filter_comm_mode"]
        self.filter_thres_event_prim = self.params_dict["filter_thres_event_prim"]
        self.filter_thres_event_sec = self.params_dict["filter_thres_event_sec"]
        self.filter_thres_bad_slopes = self.params_dict["filter_thres_bad_slopes"]

        # get parameters from data_h5 file
        total_frames_offnoi, column_size_offnoi, row_size_offnoi, nreps_offnoi = (
            io.get_params_from_data_file(self.offnoi_data_file)
        )
        total_frames_filter, column_size_filter, row_size_filter, nreps_filter = (
            io.get_params_from_data_file(self.filter_data_file)
        )
        # check if sensor size is equal
        if (
            column_size_offnoi != column_size_filter
            or row_size_offnoi != row_size_filter
        ):
            raise ValueError(
                "Column size or row size of offnoi and filter data files are not equal."
            )

        self.column_size = column_size_offnoi
        self.row_size = row_size_offnoi
        # set total number of frames and nreps from the data file
        self.offnoi_total_nreps = nreps_offnoi
        self.offnoi_total_frames = total_frames_offnoi
        self.filter_total_nreps = nreps_filter
        self.filter_total_frames = total_frames_filter

        # nreps_eval and nframes_eval is [start,stop,step], if stop is -1 it goes to the end
        if self.offnoi_nframes_eval[1] == -1:
            self.offnoi_nframes_eval[1] = self.offnoi_total_frames
        if self.offnoi_nreps_eval[1] == -1:
            self.offnoi_nreps_eval[1] = self.offnoi_total_nreps
        if self.filter_nframes_eval[1] == -1:
            self.filter_nframes_eval[1] = self.filter_total_frames
        if self.filter_nreps_eval[1] == -1:
            self.filter_nreps_eval[1] = self.filter_total_nreps

        # create slices for retrieval of data from the data file
        # loading from h5 doesnt work with numpy sling notation, so we have to create slices
        self.offnoi_nreps_slice = slice(*self.offnoi_nreps_eval)
        self.offnoi_nframes_slice = slice(*self.offnoi_nframes_eval)
        self.filter_nreps_slice = slice(*self.filter_nreps_eval)
        self.filter_nframes_slice = slice(*self.filter_nframes_eval)

        # set variables to number of nreps_eval and nframes_eval to be evaluated (int)
        self.offnoi_nreps_eval = int(
            (self.offnoi_nreps_eval[1] - self.offnoi_nreps_eval[0])
            / self.offnoi_nreps_eval[2]
        )
        self.offnoi_nframes_eval = int(
            (self.offnoi_nframes_eval[1] - self.offnoi_nframes_eval[0])
            / self.offnoi_nframes_eval[2]
        )
        self.filter_nreps_eval = int(
            (self.filter_nreps_eval[1] - self.filter_nreps_eval[0])
            / self.filter_nreps_eval[2]
        )
        self.filter_nframes_eval = int(
            (self.filter_nframes_eval[1] - self.filter_nframes_eval[0])
            / self.filter_nframes_eval[2]
        )

        # check, if offnoi_nreps_eval is greater or equal than filter_nreps_eval
        # this is necessary, because the filter step needs the offset_raw from the offnoi step
        if self.offnoi_nreps_eval < self.filter_nreps_eval:
            raise ValueError(
                "offnoi_nreps_eval must be greater or equal than filter_nreps_eval"
            )

        # create analysis h5 file
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        bin_filename = os.path.basename(self.offnoi_data_file)[:-3]
        self.analysis_file_name = f"{timestamp}_{bin_filename}.h5"
        self.analysis_file = os.path.join(self.results_dir, self.analysis_file_name)
        io.create_analysis_file(
            self.results_dir,
            self.analysis_file_name,
            self.offnoi_data_file,
            self.filter_data_file,
            self.params_dict,
        )
        self._logger.info(
            f"Created analysis h5 file: {self.results_dir}/{self.analysis_file_name}"
        )
        self._logger.info(f"Parameters loaded:")
        self.params.print_contents()

    def calc_offnoi_step(self) -> None:

        estimated_ram_usage = (
            utils.get_ram_usage_in_gb(
                self.offnoi_nframes_eval,
                self.column_size,
                self.offnoi_nreps_eval,
                self.row_size,
            )
            * 2.5  # this is estimated, better safe than sorry
        )

        self._logger.info(f"---------Start offnoi step---------")
        self._logger.info(f"RAM available: {self.ram_available:.1f} GB")
        self._logger.info(f"Estimated RAM usage: {estimated_ram_usage:.1f} GB")
        steps_needed = int(estimated_ram_usage / self.ram_available) + 1
        self._logger.info(f"Steps needed: {steps_needed}")

        # (planned) frames per step, so that ram usage is below the available ram
        frames_per_step = int(self.offnoi_nframes_eval / steps_needed)

        # total processed frames over all steps
        total_frames_processed = 0

        """
        Start of the loop to process the data in steps, so that the ram usage is below the available ram
        -removed mips and bad frames for now
        """
        for step in range(steps_needed):
            self._logger.info(f"Start processing step {step+1} of {steps_needed}")
            current_frame_slice = slice(
                total_frames_processed,
                total_frames_processed + frames_per_step,
            )
            slices = [
                current_frame_slice,
                slice(None),
                self.offnoi_nreps_slice,
                slice(None),
            ]
            data = (
                io.get_data_from_file(self.offnoi_data_file, "data", slices)
                * self.polarity
            )
            self._logger.info(f"Data loaded: {data.shape}")
            if self.offnoi_comm_mode is True:
                an.correct_common_mode(data)
            avg_over_nreps = utils.get_avg_over_nreps(data)
            io.add_array(
                self.analysis_file,
                "offnoi/precal/rndr_signals_after_common",
                avg_over_nreps,
            )
            if self.offnoi_thres_bad_slopes != 0:
                slopes = an.get_slopes(data)
                io.add_array(self.analysis_file, "offnoi/slopes/all_frames", slopes)
            total_frames_processed += frames_per_step
            self._logger.info(f"Finished step {step+1} of {steps_needed} total Steps")

        self._logger.info("Start calculating bad slopes")
        slopes = io.get_data_from_file(self.analysis_file, "offnoi/slopes/all_frames")
        fitted = fit.get_pixelwise_fit(slopes, peaks=1)
        lower_bound = fitted[:, :, 1] - self.offnoi_thres_bad_slopes * np.abs(
            fitted[:, :, 2]
        )
        upper_bound = fitted[:, :, 1] + self.offnoi_thres_bad_slopes * np.abs(
            fitted[:, :, 2]
        )
        bad_slopes_mask = (slopes < lower_bound) | (slopes > upper_bound)
        io.add_array(self.analysis_file, "offnoi/slopes/fit/amplitude", fitted[:, :, 0])
        io.add_array(self.analysis_file, "offnoi/slopes/fit/mean", fitted[:, :, 1])
        io.add_array(self.analysis_file, "offnoi/slopes/fit/sigma", fitted[:, :, 2])
        io.add_array(
            self.analysis_file, "offnoi/slopes/fit/error_amplitude", fitted[:, :, 3]
        )
        io.add_array(
            self.analysis_file, "offnoi/slopes/fit/error_mean", fitted[:, :, 4]
        )
        io.add_array(
            self.analysis_file, "offnoi/slopes/fit/error_sigma", fitted[:, :, 5]
        )
        io.add_array(
            self.analysis_file, "offnoi/slopes/bad_slopes_mask", bad_slopes_mask
        )
        io.add_array(
            self.analysis_file,
            "offnoi/slopes/bad_slopes_count",
            np.sum(bad_slopes_mask, axis=0),
        )
        failed_fits = np.sum(np.isnan(fitted[:, :, 1]))
        if failed_fits > 0:
            self._logger.warning(
                f"Failed fits: {failed_fits} ({failed_fits/(self.column_size*self.row_size)*100:.2f}%)"
            )

        # get avg_over_nreps from the loop
        avg_over_nreps = io.get_data_from_file(
            self.analysis_file, "offnoi/precal/rndr_signals_after_common"
        )
        # set bad slopes to nan, so they not interfere in future calculations
        avg_over_nreps[bad_slopes_mask] = np.nan
        io.add_array(
            self.analysis_file,
            "offnoi/precal/rndr_signals_after_common_slopes_removed",
            avg_over_nreps,
        )
        bad_signals = np.sum(bad_slopes_mask)
        self._logger.warning(
            f"Signals removed due to bad slopes: {bad_signals} ({bad_signals/(bad_slopes_mask.size)*100:.2f}%)"
        )
        self._logger.info("Finished calculating bad slopes")

        # TODO: check if this preliminary fit is useful
        self._logger.info("Start preliminary fit to remove outliers")
        fitted = fit.get_pixelwise_fit(avg_over_nreps, peaks=1)
        io.add_array(self.analysis_file, "offnoi/prelim_fit/amplitude", fitted[:, :, 0])
        io.add_array(self.analysis_file, "offnoi/prelim_fit/mean", fitted[:, :, 1])
        io.add_array(self.analysis_file, "offnoi/prelim_fit/sigma", fitted[:, :, 2])
        io.add_array(
            self.analysis_file, "offnoi/prelim_fit/error_amplitude", fitted[:, :, 3]
        )
        io.add_array(
            self.analysis_file, "offnoi/prelim_fit/error_mean", fitted[:, :, 4]
        )
        io.add_array(
            self.analysis_file, "offnoi/prelim_fit/error_sigma", fitted[:, :, 5]
        )
        lower_bound = fitted[:, :, 1] - 8 * fitted[:, :, 2]
        upper_bound = fitted[:, :, 1] + 8 * fitted[:, :, 2]
        prelim_fit_mask = (avg_over_nreps < lower_bound) | (
            avg_over_nreps > upper_bound
        )
        avg_over_nreps[prelim_fit_mask] = np.nan
        io.add_array(
            self.analysis_file,
            "offnoi/prelim_fit/prelim_fit_mask",
            prelim_fit_mask,
        )
        failed_fits = np.sum(np.isnan(fitted[1, :, :]))
        if failed_fits > 0:
            self._logger.warning(
                f"Failed fits: {failed_fits} ({failed_fits/(self.column_size*self.row_size)*100:.2f}%)"
            )
        bad_signals = np.sum(prelim_fit_mask)
        self._logger.warning(
            f"Signals removed due to preliminary fit: {bad_signals} ({bad_signals/(prelim_fit_mask.size)*100:.2f}%)"
        )
        self._logger.info("Finished preliminary fit to remove outliers")

        self._logger.info("Start fitting 1 peak gaussian to determine offset")
        fitted = fit.get_pixelwise_fit(avg_over_nreps, peaks=1)
        io.add_array(self.analysis_file, "offnoi/fit/amplitude1", fitted[:, :, 0])
        io.add_array(self.analysis_file, "offnoi/fit/mean1", fitted[:, :, 1])
        io.add_array(self.analysis_file, "offnoi/fit/sigma1", fitted[:, :, 2])
        io.add_array(self.analysis_file, "offnoi/fit/error_amplitude1", fitted[:, :, 3])
        io.add_array(self.analysis_file, "offnoi/fit/error_mean1", fitted[:, :, 4])
        io.add_array(self.analysis_file, "offnoi/fit/error_sigma1", fitted[:, :, 5])
        failed_fits = np.sum(np.isnan(fitted[:, :, 1]))
        if failed_fits > 0:
            self._logger.warning(
                f"Failed fits: {failed_fits} ({failed_fits/(self.column_size*self.row_size)*100:.2f}%)"
            )
        self._logger.info("Finished fitting 1 peak gaussian to determine offset")

        self._logger.info("Offset data and save rndr_signals")
        avg_over_nreps -= fitted[:, :, 1]
        io.add_array(
            self.analysis_file,
            "offnoi/rndr_signals/all_frames",
            avg_over_nreps,
        )
        self._logger.info("Finished offsetting data and saving rndr_signals")
        self._logger.info("---------Finished offnoi step---------")

    def calc_filter_step(self) -> None:
        estimated_ram_usage = (
            utils.get_ram_usage_in_gb(
                self.filter_nframes_eval,
                self.column_size,
                self.filter_nreps_eval,
                self.row_size,
            )
            * 2.5  # this is estimated, better safe than sorry
        )
        self._logger.info(f"---------Start filter step---------")
        self._logger.info(f"RAM available: {self.ram_available:.1f} GB")
        self._logger.info(f"Estimated RAM usage: {estimated_ram_usage:.1f} GB")
        steps_needed = int(estimated_ram_usage / self.ram_available) + 1
        self._logger.info(f"Steps needed: {steps_needed}")

        # (planned) frames per step, so that ram usage is below the available ram
        frames_per_step = int(self.filter_nframes_eval / steps_needed)

        # total processed frames over all steps
        total_frames_processed = 0

        """
        Start of the loop to process the data in steps, so that the ram usage is below the available ram
        -removed mips and bad frames for now
        """
        for step in range(steps_needed):
            self._logger.info(f"Start processing step {step+1} of {steps_needed}")
            current_frame_slice = slice(
                total_frames_processed,
                total_frames_processed + frames_per_step,
            )
            slices = [
                current_frame_slice,
                slice(None),
                self.filter_nreps_slice,
                slice(None),
            ]
            data = (
                io.get_data_from_file(self.filter_data_file, "data", slices)
                * self.polarity
            )
            self._logger.info(f"Data loaded: {data.shape}")
            if self.filter_comm_mode is True:
                an.correct_common_mode(data)
            avg_over_nreps = utils.get_avg_over_nreps(data)
            io.add_array(
                self.analysis_file,
                "filter/precal/rndr_signals_after_common",
                avg_over_nreps,
            )
            fitted_offset = io.get_data_from_file(
                self.analysis_file, "offnoi/fit/mean1"
            )
            avg_over_nreps -= fitted_offset
            io.add_array(
                self.analysis_file, "filter/rndr_signals/all_frames", avg_over_nreps
            )
            if self.filter_thres_bad_slopes != 0:
                slopes = an.get_slopes(data)
                io.add_array(self.analysis_file, "filter/slopes/all_frames", slopes)
            total_frames_processed += frames_per_step
            self._logger.info(f"Finished step {step+1} of {steps_needed} total Steps")

        self._logger.info("Start calculating bad slopes")
        slopes = io.get_data_from_file(self.analysis_file, "filter/slopes/all_frames")
        fitted = fit.get_pixelwise_fit(slopes, peaks=1)
        lower_bound = fitted[:, :, 1] - self.filter_thres_bad_slopes * np.abs(
            fitted[:, :, 2]
        )
        upper_bound = fitted[:, :, 1] + self.filter_thres_bad_slopes * np.abs(
            fitted[:, :, 2]
        )
        bad_slopes_mask = (slopes < lower_bound) | (slopes > upper_bound)
        io.add_array(self.analysis_file, "filter/slopes/fit/amplitude", fitted[:, :, 0])
        io.add_array(self.analysis_file, "filter/slopes/fit/mean", fitted[:, :, 1])
        io.add_array(self.analysis_file, "filter/slopes/fit/sigma", fitted[:, :, 2])
        io.add_array(
            self.analysis_file, "filter/slopes/fit/error_amplitude", fitted[:, :, 3]
        )
        io.add_array(
            self.analysis_file, "filter/slopes/fit/error_mean", fitted[:, :, 4]
        )
        io.add_array(
            self.analysis_file, "filter/slopes/fit/error_sigma", fitted[:, :, 5]
        )
        io.add_array(
            self.analysis_file, "filter/slopes/bad_slopes_mask", bad_slopes_mask
        )
        io.add_array(
            self.analysis_file,
            "filter/slopes/bad_slopes_count",
            np.sum(bad_slopes_mask, axis=0),
        )
        failed_fits = np.sum(np.isnan(fitted[:, :, 1]))
        if failed_fits > 0:
            self._logger.warning(
                f"Failed fits: {failed_fits} ({failed_fits/(self.column_size*self.row_size)*100:.2f}%)"
            )

        # load avg_over_nreps from the loop
        avg_over_nreps = io.get_data_from_file(
            self.analysis_file, "filter/rndr_signals/all_frames"
        )
        # set bad slopes to nan, so they not interfere in future calculations
        avg_over_nreps[bad_slopes_mask] = np.nan
        io.add_array(
            self.analysis_file,
            "filter/rndr_signals/all_frames_slopes_removed",
            avg_over_nreps,
        )
        bad_signals = np.sum(bad_slopes_mask)
        self._logger.warning(
            f"Signals removed due to bad slopes: {bad_signals} ({bad_signals/(bad_slopes_mask.size)*100:.2f}%)"
        )
        self._logger.info("Finished calculating bad slopes")

        self._logger.info("Start preliminary fit to remove outliers")
        fitted = fit.get_pixelwise_fit(avg_over_nreps, peaks=1)
        io.add_array(self.analysis_file, "filter/prelim_fit/amplitude", fitted[:, :, 0])
        io.add_array(self.analysis_file, "filter/prelim_fit/mean", fitted[:, :, 1])
        io.add_array(self.analysis_file, "filter/prelim_fit/sigma", fitted[:, :, 2])
        io.add_array(
            self.analysis_file, "filter/prelim_fit/error_amplitude", fitted[:, :, 3]
        )
        io.add_array(
            self.analysis_file, "filter/prelim_fit/error_mean", fitted[:, :, 4]
        )
        io.add_array(
            self.analysis_file, "filter/prelim_fit/error_sigma", fitted[:, :, 5]
        )
        lower_bound = fitted[:, :, 1] - 8 * fitted[:, :, 2]
        upper_bound = fitted[:, :, 1] + 8 * fitted[:, :, 2]
        prelim_fit_mask = (avg_over_nreps < lower_bound) | (
            avg_over_nreps > upper_bound
        )
        avg_over_nreps[prelim_fit_mask] = np.nan
        io.add_array(
            self.analysis_file,
            "filter/prelim_fit/prelim_fit_mask",
            prelim_fit_mask,
        )
        io.add_array(
            self.analysis_file,
            "filter/rndr_signals/all_frames_slopes_removed_prelim_fit",
            avg_over_nreps,
        )
        failed_fits = np.sum(np.isnan(fitted[1, :, :]))
        if failed_fits > 0:
            self._logger.warning(
                f"Failed fits: {failed_fits} ({failed_fits/(self.column_size*self.row_size)*100:.2f}%)"
            )
        bad_signals = np.sum(prelim_fit_mask)
        self._logger.warning(
            f"Signals removed due to preliminary fit: {bad_signals} ({bad_signals/(prelim_fit_mask.size)*100:.2f}%)"
        )
        self._logger.info("Finished preliminary fit to remove outliers")

        self._logger.info("Start Calculating event_map")
        noise_map = io.get_data_from_file(self.analysis_file, "offnoi/fit/sigma1")
        structure = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        event_array = an.group_pixels(
            avg_over_nreps,
            self.filter_thres_event_prim,
            self.filter_thres_event_sec,
            noise_map,
            structure,
        )
        io.add_array(self.analysis_file, "filter/events/event_map", event_array)
        io.add_array(
            self.analysis_file,
            "filter/events/event_map_counts",
            np.sum(event_array != 0, axis=0),
        )
        self._logger.info("Finished calculating event_map")
        self._logger.info("---------Finished filter step---------")

    def calc_gain_step(self) -> None:
        self._logger.info("---------Start gain step---------")
        self._logger.info("Start fitting 1 peak gaussian for gain calculation")
        avg_over_nreps = io.get_data_from_file(
            self.analysis_file,
            "filter/rndr_signals/all_frames_slopes_removed_prelim_fit",
        )
        fitted = fit.get_pixelwise_fit(avg_over_nreps, peaks=1)
        io.add_array(self.analysis_file, "gain/fit/amplitude1", fitted[:, :, 0])
        io.add_array(self.analysis_file, "gain/fit/mean1", fitted[:, :, 1])
        io.add_array(self.analysis_file, "gain/fit/sigma1", fitted[:, :, 2])
        io.add_array(self.analysis_file, "gain/fit/error_amplitude1", fitted[:, :, 3])
        io.add_array(self.analysis_file, "gain/fit/error_mean1", fitted[:, :, 4])
        io.add_array(self.analysis_file, "gain/fit/error_sigma1", fitted[:, :, 5])
        self._logger.info("Finished fitting 1 peak gaussian for gain calculation")
        self._logger.info("---------Finished gain step---------")

from tkinter import messagebox as mb
import numpy as np
import os
import warnings

warnings.simplefilter("error", RuntimeWarning)

# caught in mainfile
try:
    from pydub import AudioSegment
except RuntimeWarning:
    # passing to allow capture and quit in executable
    pass


# validate user inputs for degrade settings
def input_validate(sample_rate, bit_rate, normalize_set):
    if (
        sample_rate == "Source"
        and bit_rate == "Source"
        and normalize_set is False
    ):
        mb.showerror(message="You need to select a degrade setting!")
        raise RuntimeError

    # checking sample rate settings
    if sample_rate != "Source":
        if not sample_rate.isnumeric():
            mb.showerror(
                message="Invalid input in sample rate field!"
                + "\n\nSample rate needs to be set between 300 and 48000"
                + "\n\nNumeric only (no ',' or '.')"
            )
            raise TypeError
        elif int(sample_rate) > 48000 or int(sample_rate) < 300:
            mb.showerror(
                message="Sample rate needs to be set between 300 and 48000"
            )
            raise ValueError
        elif int(sample_rate) >= 300 and int(sample_rate) < 4000:
            if (
                mb.askyesno(
                    message="Warning!\n"
                    + "Sample Rates below 4000 are likely"
                    + " to cause compatibility issues"
                    + "\n\nAre you sure you wish to continue?"
                )
                is False
            ):
                raise RuntimeError


# check if output directoy exists and is directory; if not create it
def dir_check(output_directory):
    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
        except PermissionError:
            mb.showerror(
                message=(
                    "Permissions error occured when creating directorys!"
                    + "\n\nCheck output directory permissions and try again"
                )
            )
            raise PermissionError
        # passes to next check for paths with ending '/'
        except NotADirectoryError:
            pass

    # checks if a file with matched pathname exists
    if not os.path.isdir(output_directory):
        mb.showerror(
            message=(
                "A file exists with the same name as the output directory\n\n"
                + "Delete/move file or select a different output directory"
            )
        )
        raise NotADirectoryError


# checking for overwrites
def overwrite_check(
    overwrite_filename, overwrite_cnt, overwrite_all, lst_length
):
    if (
        mb.askyesno(
            message=(
                "File '"
                + overwrite_filename
                + "' exists, do you want to overwrite?"
            ),
            icon="question",
            title="Overwrite?",
        )
        is False
    ):
        raise FileExistsError
    else:
        overwrite_cnt = overwrite_cnt + 1

    # giving user option to overwrite all, repeats every 5th time
    if overwrite_cnt % 5 == 1 and lst_length > "1":
        if (
            mb.askyesno(
                message=("Do you want to overwrite all?"),
                icon="question",
                title="Overwrite all?",
            )
            is True
        ):
            overwrite_all = True

    return overwrite_cnt, overwrite_all


# file opening function
def file_open(file_format, file_path):
    if file_format == ".wav":
        infile = AudioSegment.from_wav(file_path)
    elif file_format == ".mp3":
        infile = AudioSegment.from_mp3(file_path)
    elif file_format == ".aif" or file_format == ".aiff":
        infile = AudioSegment.from_file(file_path, "aiff")

    return infile


# sample rate conversion function
def sample_rate_conv(audio_file, sample_rate):
    # conversion process
    sample_rate = int(sample_rate)
    if audio_file.frame_rate < sample_rate:
        raise ValueError("input file below desired sample rate")

    converted_file = audio_file.set_frame_rate(sample_rate)
    return converted_file


# bit rate conversion that actually changes the encoding of the file to 8 bits
def bit_actual_conv(audio_file):
    if audio_file.sample_width <= 1:
        raise ValueError("input file below desired bit rate")

    converted_file = audio_file.set_sample_width(1)
    return converted_file


# bit shifting bit rate conversion (default bitrate setting)
def bit_shift_conv(audio_file, bit_rate):
    # setting vars and checking for lower bitrate input
    src_bitrate = (
        audio_file.sample_width * 8
    )  # sample_width returns bytes in a sample, * 8 = bit rate
    br_diff = src_bitrate - bit_rate
    if br_diff <= 0:
        raise ValueError("input file below desired bit rate")

    # bit shift process
    sample_array = audio_file.get_array_of_samples()
    r_shift_array = np.right_shift(sample_array, br_diff)
    padded_array = np.left_shift(r_shift_array, br_diff)
    converted_file = audio_file._spawn(padded_array)
    return converted_file


# signal to noise ratio bit rate conversion (alternate bitrate setting)
def bit_db_conv(audio_file, bit_rate):
    # setting vars and checking for lower bitrate input
    # sample_width returns bytes in a sample, * 8 = bit rate
    src_bitrate = audio_file.sample_width * 8
    # bit rate * six = signal noise ratio
    snr_diff = (src_bitrate * 6) - (bit_rate * 6)
    if snr_diff <= 0:
        raise ValueError("input file below desired bit rate")

    # conversion process
    # decimates by removing the difference and padding back
    converted_file = (audio_file - snr_diff) + snr_diff
    return converted_file

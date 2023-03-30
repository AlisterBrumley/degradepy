# you will need to install pydub, numpy and ffmpeg to run
# some built in installations of python are also missing tkinter
# and will additionally need that installed to run
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import os
import deghelpers as deg
import guihelpers as gh
from datetime import datetime as dt
import warnings

warnings.simplefilter("error", RuntimeWarning)

# if ffmpeg is missing notify the user and quit
try:
    from pydub.effects import normalize
except RuntimeWarning:
    mb.showwarning(message="ffmpeg not found!\n\nInstall ffmpeg and ffprobe to run")
    print("Python RuntimeWarning: ffmpeg not found!")
    exit()


# main degrade function
def degrade():
    # setting variables
    sample_rate = sr_list.get()
    bit_rate = br_list.get()
    out_format = out_format_sv.get()
    output_dir = out_directory_sv.get()
    nrml_set = normalize_set_bv.get()
    list_length = str(len(file_list))
    overwrite_all = False
    overwrite_count = 0

    # forcing input
    if list_length == "0":
        mb.showerror(message="Need to select files!")
        return

    # checking degrade settings
    try:
        deg.input_validate(sample_rate, bit_rate, nrml_set)
    except (TypeError, ValueError, RuntimeError):
        return

    # confirm with user about the amount of files they are creating
    if (
        mb.askyesno(
            message=("Are you sure you want to degrade " + list_length + " files?"),
            icon="question",
            title="Confirmation",
        )
        is False
    ):
        return

    # directory checking/creating
    if len(output_dir) > 0:
        try:
            deg.dir_check(output_dir)
        except (PermissionError, NotADirectoryError):
            return

    # loop for iterating over files
    for file_path in file_list:

        # setting varibles
        # if output directory not set, use the original's directory
        if len(output_dir) == 0:
            output_dir = os.path.dirname(file_path)
        filename, in_format = os.path.splitext(os.path.basename(file_path))

        # set output filename
        out_filename = output_dir + "/" + filename + ".deg." + out_format

        # checking overwrites
        if os.path.exists(out_filename) and not overwrite_all:
            try:
                overwrite_count, overwrite_all = deg.overwrite_check(
                    out_filename, overwrite_count, overwrite_all, list_length
                )
            except FileExistsError:
                return

        # conversion implementation
        # file opening
        try:
            conv_temp_file = deg.file_open(in_format, file_path)
        except Exception as exc:
            print("FILE OPEN ERROR WITH: " + filename + in_format)
            print(exc)
            try:
                err_log = open("ERROR_LOG.txt", "a")
                err_log.write("\n\nEntry at " + str(dt.now()) + "\n" + str(exc))
                err_log.close
                print("ERROR LOGGED")
                mb.showerror(
                    message=(
                        filename
                        + in_format
                        + " file open error, check ERROR_LOG.txt for details"
                        + "\n\nfile will be skipped!"
                    )
                )
                continue
            except PermissionError:
                print("PERMISSION ERROR: COULD NOT CREATE/APPEND ERROR LOG")
                mb.showerror(
                    message=(
                        filename
                        + in_format
                        + " file open error: error log could not be created"
                        + " or written to due to permissions issues"
                        + "\n\nfile will be skipped!"
                    )
                )
                continue

        # conversion and normalization process
        if normalize_set_bv.get() is True:
            conv_temp_file = normalize(conv_temp_file, 3)

        # sample rate conversion
        if not sample_rate == "Source":
            try:
                conv_temp_file = deg.sample_rate_conv(conv_temp_file, int(sample_rate))
            except ValueError:
                mb.showerror(
                    message=filename
                    + in_format
                    + " is already below the selected sample rate"
                    + "\n\nsample rate conversion will be skipped"
                )

        # bit rate conversion
        try:
            if bit_rate == "Source":
                outfile = conv_temp_file
            elif bit_rate == "8 (actual)":
                outfile = deg.bit_actual_conv(conv_temp_file)
            elif alt_br_set_bv.get() is True:
                outfile = deg.bit_db_conv(conv_temp_file, int(bit_rate))
            else:
                outfile = deg.bit_shift_conv(conv_temp_file, int(bit_rate))
        except ValueError:
            mb.showerror(
                message=filename
                + in_format
                + " is already below the selected bit rate"
                + "\n\nbit rate conversion will be skipped"
            )
            outfile = conv_temp_file

        # export file
        try:
            outfile.export(out_filename, format=out_format)
        except PermissionError:
            mb.showerror(
                message="Permission error when writing files"
                + "\n\nCheck output directory permissions and try again"
            )
            return

    # clearing list and notifying user
    gh.clear_list(file_list_sv, file_list)
    mb.showinfo(message="degrade complete!")


# main window setup
main_window = tk.Tk()
main_window.title("QnD Wave Degrade")
main_window.resizable(False, False)

# variable settings
file_list = []
out_sr_sv = tk.StringVar(value="Source")
out_br_sv = tk.StringVar(value="Source")
normalize_set_bv = tk.BooleanVar()
alt_br_set_bv = tk.BooleanVar()
file_list_sv = tk.StringVar()
out_format_sv = tk.StringVar(value="wav")
out_directory_sv = tk.StringVar()

# window frames
com_box_frame = ttk.Frame(main_window, padding=5)
com_box_frame.pack()
list_frame = ttk.Frame(main_window, padding=(10, 10, 10, 1))
list_frame.pack()
lst_btn_frame = ttk.Frame(main_window)
lst_btn_frame.pack()
out_dir_frame = ttk.Frame(main_window)
out_dir_frame.pack(pady=10)
deg_btn_frame = ttk.Frame(main_window)
deg_btn_frame.pack()

# # window visible content
# labels
sr_label = ttk.Label(com_box_frame, text="Select Sample Rate")
sr_label.grid(row=1, column=0, pady=(15, 5))

br_label = ttk.Label(com_box_frame, text='Select "Bit Rate"')
br_label.grid(row=1, column=1, pady=(15, 5))

# comboboxes
sr_list = ttk.Combobox(
    com_box_frame,
    textvariable=out_sr_sv,
    values=("Source", 44100, 32000, 22050, 16000, 11025, 8000, 5512, 4000),
)
sr_list.grid(row=2, column=0)
sr_list.grid_configure(padx=10)
br_list = ttk.Combobox(
    com_box_frame,
    textvariable=out_br_sv,
    values=("Source", 16, 12, 8, "8 (actual)"),
    state="readonly",
)
br_list.grid(row=2, column=1)
br_list.grid_configure(padx=10)

# checkboxes
normalize_check = ttk.Checkbutton(
    com_box_frame,
    text="Normalize Before Degrade",
    variable=normalize_set_bv,
    onvalue=True,
    offvalue=False,
)
normalize_check.grid(row=1, column=2, sticky=tk.SW)
alt_br_check = ttk.Checkbutton(
    com_box_frame,
    text="Alternate Bitrate Conversion",
    variable=alt_br_set_bv,
    onvalue=True,
    offvalue=False,
)
alt_br_check.grid(row=2, column=2, sticky=tk.W)

# lists and scrollbars
v_scroll = ttk.Scrollbar(list_frame, orient="vertical")
h_scroll = ttk.Scrollbar(list_frame, orient="horizontal")
gui_file_list = tk.Listbox(
    list_frame,
    listvariable=file_list_sv,
    selectmode="extended",
    width=70,
    height=20,
    xscrollcommand=h_scroll.set,
    yscrollcommand=v_scroll.set,
)
gui_file_list.grid(row=0, column=0)
v_scroll.config(command=gui_file_list.yview)
v_scroll.grid(row=0, column=1, sticky=tk.NS)
h_scroll.config(command=gui_file_list.xview)
h_scroll.grid(row=1, column=0, sticky=tk.EW)

# file i/o ttk.buttons
file_open_btn = ttk.Button(
    lst_btn_frame,
    text="Select Files",
    command=lambda: gh.select_files(file_list_sv, file_list),
)
file_open_btn.grid(row=0, column=0, pady=(0, 10), padx=10)
file_remove_btn = ttk.Button(
    lst_btn_frame,
    text="Remove Selected",
    command=lambda: gh.remove_file(file_list_sv, file_list, gui_file_list),
)
file_remove_btn.grid(row=0, column=1, pady=(0, 10), padx=10)
file_list_clear_btn = ttk.Button(
    lst_btn_frame,
    text="Remove All",
    command=lambda: gh.clear_list(file_list_sv, file_list),
)
file_list_clear_btn.grid(row=0, column=2, pady=(0, 10), padx=10)

# file output field/select
out_dir_btn = ttk.Button(
    out_dir_frame,
    text="Select Output Directory",
    command=lambda: gh.select_out_dir(out_directory_sv),
)
out_dir_btn.grid(row=1, column=0, padx=10)
out_dir_field = ttk.Entry(out_dir_frame, width=40, textvariable=out_directory_sv)
out_dir_field.grid(row=1, column=1)

# degrade ttk.button
aif_check = ttk.Checkbutton(
    deg_btn_frame,
    text="Export as AIFF",
    variable=out_format_sv,
    onvalue="aiff",
    offvalue="wav",
)
aif_check.grid(row=0, column=0, pady=(5, 0))
degrade_btn = ttk.Button(deg_btn_frame, text="Degrade", command=degrade)
degrade_btn.grid(row=1, column=0, pady=(5, 0))

# version number
# currently 6th beta
version_no = ttk.Label(main_window, text="v0.7beta")
version_no.pack(side="right")

# window main function
main_window.mainloop()

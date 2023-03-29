from tkinter import filedialog as fd


# file select
def select_files(file_list_sv, file_list):
    # limiting what files can be opened
    file_types = [
        ("Audio Files", "*.wav *.mp3 *.aiff *.aif"),
        ("WAV files", "*.wav"),
        ("AIFF files", "*.aiff *.aif"),
        ("MP3 files", "*.mp3"),
    ]

    # dialog box for selecting files
    files_selected = fd.askopenfilenames(
        title="Select Files for Conversion",
        initialdir=".",
        filetypes=file_types,
    )

    # if user clicks cancel button
    selection_length = len(files_selected)
    if selection_length == 0:
        return

    # adding files to list and update in gui
    for file in files_selected:
        if file not in file_list:
            file_list.append(file)
    list_update(file_list_sv, file_list)


# file list select removal
def remove_file(file_list_sv, file_list, gui_file_list):
    # return if list empty
    if len(file_list) == 0:
        return

    remove_list = []

    # take file(s) selected by cursor
    try:
        for idx in gui_file_list.curselection():
            remove_list.append(file_list[idx])
    except IndexError:
        return

    # remove from list
    for file in remove_list:
        if file in file_list:
            file_list.remove(file)

    list_update(file_list_sv, file_list)


# file list clear and update in gui
def clear_list(file_list_sv, file_list):
    file_list.clear()
    list_update(file_list_sv, file_list)


# out directory select
def select_out_dir(out_directory_sv):
    # dialog box for directory select
    out_directory = fd.askdirectory(
        title="Select Output Directory", initialdir="."
    )

    # return if cancel
    op_dir_length = len(out_directory)
    if op_dir_length == 0:
        return

    # set directory in main variable
    out_directory_sv.set(out_directory)


# function to update list
def list_update(file_list_sv, file_list):
    file_list_sv.set(file_list)

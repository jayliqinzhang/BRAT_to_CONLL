import glob
import re


def process_ann(filename_ann):
    """
    Process the ann file.
    Handle the strings belonging to the argument components.

    Return:
    List: a list of tuples in format ('a', 1, arg_type), representing the a character, its index, and its arg type.
    List: a list of index numbers that are in arguments, which is used to know the non-arguments index number.

    """

    # allLines = []
    with open(filename_ann) as file:
        allLines = [re.split(r"\t+", line.rstrip("\t")) for line in file]

        # for line in file:
        #     allLines.append(re.split(r'\t+', line.rstrip('\t')))

    # Only get the component annotations tag.
    T_allLines = [comp for comp in allLines if comp[0].startswith("T")]

    # Sort the line according to the index of the entity (component).
    # The order is based on the the last index of an entity.
    sortedLinesFinal = sorted(T_allLines, key=lambda x: int(x[1].split()[2]))

    ## A list if entries containing the character, the index of the character, and argument type.
    ## ('a', 1, arg_type)
    entry_cha_index_list = []
    for eachEntity in sortedLinesFinal:

        ## The eachEntity that are shorter than 2 are relations entity rather than argument type.
        if len(eachEntity) > 2:
            ## Set the arg_type as 'B-' at the beginning.
            arg_type = "B-" + eachEntity[1].split()[0]

            # for all the strings in an entity.
            for i in range(len(eachEntity[2])):
                if eachEntity[2][i] != "\n" and eachEntity[2][i] != " ":
                    entry_cha_index_list.append(
                        (eachEntity[2][i], int(eachEntity[1].split()[1]) + i, arg_type)
                    )

                ## As long as we see a ' ', we change the arg_type to 'I-'
                if eachEntity[2][i] == " ":
                    entry_cha_index_list.append(
                        (eachEntity[2][i], int(eachEntity[1].split()[1]) + i, arg_type)
                    )
                    arg_type = "I-" + eachEntity[1].split()[0]

    ## Get the index ranges that are the arguments.
    arg_index_range = [entry[1].split()[1:] for entry in sortedLinesFinal]
    arg_index_range = [range(int(nr[0]), int(nr[1])) for nr in arg_index_range]

    ## The joint_range is a list of index numbers that are in arguments.
    joint_range = []
    for range_ in arg_index_range:
        joint_range = joint_range + list(range_)

    return entry_cha_index_list, joint_range


def process_txt(filename_txt, joint_range):
    """
    Process the txt file and handle non argument strings.
    The input of joine_range is one of the outputs from process_ann,
    so that we can get the indices that are not in arguments.

    Return:
        List: A list of tuples (txt,index,'O'). the none_character_index_list.

    """
    # Handle non argument strings.
    with open(filename_txt) as f:
        txt_string = f.read()

    ## The character that are not in the argument components.
    none_character_index_list = []
    for i in range(len(txt_string)):
        if i not in joint_range:
            none_character_index_list.append((txt_string[i], i, "O"))

    return none_character_index_list


def get_char_index(filename_txt, filename_ann):
    """
    Return:
        List of tupels in format (character_string, index, tag), and the order is sorted based on index.
    """

    # ann_char_index and none_character_index_list are list of tuples in format:
    # (character_string, index, tag), in which tag is argument type tag or non tag.
    ann_char_index, ann_index_list = process_ann(filename_ann)
    none_character_index_list = process_txt(filename_txt, ann_index_list)

    # Join the two lists of in argument and none argument together.
    joint_cha_index = none_character_index_list + ann_char_index

    # Put the list in order based on the index of each character.
    sorted_joint_cha_index = sorted(joint_cha_index, key=lambda x: int(x[1]))

    return sorted_joint_cha_index


def get_result(filename_txt, filename_ann):
    """
    Input:
        First is the text file, second is the annotation file.
    Return:
        A list of lines that are ready to be written to a file.
    """

    sorted_joint_cha_index = get_char_index(filename_txt, filename_ann)

    # the under-processing string.
    tem = ""

    # These symbols should be handled exclusively.
    special_symbol = [" ", "\n", ",", ".", "?"]

    # This is a list of lines that are written in a file.
    write_output_line = []
    for tup in sorted_joint_cha_index:

        # handle special symbols.
        # Take the argument type of the previous one character.
        if tup[0] in special_symbol:

            arg_type = sorted_joint_cha_index[sorted_joint_cha_index.index(tup) - 1][2]
            if tem != "":
                write_output_line.append(tem + "\t" + arg_type)
            else:
                write_output_line.append(tem)
            if tup[0] == " " or tup[0] == "\n":
                tem = ""
            else:
                tem = tup[0]
        else:
            tem = tem + tup[0]

        if tup[1] == len(sorted_joint_cha_index) - 1:
            write_output_line.append(tup[0] + "\t" + tup[2])

    return write_output_line


def write_result(path, output_path):
    """
    path: the path to all the text (.txt) and brat annotation (.ann) file.
    output_path: the path where the results are written to.
    """

    file_name = [txt.split(".")[0].split("/")[1] for txt in glob.glob(f"{path}/*.txt")]

    all_output = []
    for name in file_name:
        txt_name_path = f"{path}/{name}.txt"
        ann_name_path = f"{path}/{name}.ann"
        one_essay_result = get_result(txt_name_path, ann_name_path)
        with open(f"{output_path}/{name}.conll", "w") as f:
            for entity in one_essay_result:
                f.write(entity + "\n")
        all_output.append(one_essay_result)


if __name__ == "__main__":
    write_result("sample_input_folder", "output_folder")

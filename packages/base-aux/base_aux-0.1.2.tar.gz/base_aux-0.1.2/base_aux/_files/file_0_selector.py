# TODO-1=add logdata_load_by_name_wo_extention with extention param!
# TODO-1=add extention default? maybe NO!
# TODO-1=add delete blank dirs in dicrpath
# TODO-1=add delete dirtree


# =====================================================================================================================
from typing import *
import pathlib
import datetime
import shutil


# =====================================================================================================================
class Dir:
    FILEPATH: pathlib.Path
    DIRPATH: pathlib.Path = None  # WORKING DIRECTORY like change CWD! BUT IMPORTANT! use it only for perpose if you need to find filepath in exact dirpath

    @property
    def dirpath(self) -> pathlib.Path:  # final dirpath to file #dirpath never set!!! used only in some methods!!!
        """
        created only for resolving CWD or self.FILEPATH.parent

        CAREFUL:
            1. use it only forgetting parent from setted self.FILEPATH!!!!
            if you need resolve it by passing new filepath without saving in FILEPATH use dirpath_get_active!!!!
        :return:
        """
        dirpath = None
        if self.FILEPATH:
            dirpath = self.FILEPATH.parent
        if not dirpath:
            dirpath = self.DIRPATH
        if not dirpath:
            dirpath = pathlib.Path.cwd()
        return dirpath

    def dirpath_get_active(self, dirpath: Union[None, str, pathlib.Path] = None) -> pathlib.Path:
        """
        UNDER QUESTION!
            Дефолт дирпас - актуален только если вы не знаете какой будет файл но заранее известно в какой папке!
            После установки файла дирпас идет строго по нему!!!! А после очистки файла возвращается к дефолтному!!!
            Если дефолтных не установлен то свд ???
        """
        # NOT INPUTED -------------------------------
        if dirpath is None:
            dirpath = self.DIRPATH

        # INPUTED -------------------------------
        return pathlib.Path(dirpath)

    def dirpath_ensure(self, dirpath: Union[None, str, pathlib.Path] = None) -> bool:
        dirpath = self.dirpath_get_active(dirpath=dirpath)

        try:
            dirpath.mkdir(parents=True, exist_ok=True)
        except:
            pass

        if dirpath.exists():
            return True
        else:
            msg = f"CANT create {dirpath=}"
            print(msg)

    # FIND ------------------------------------------------------------------------------------------------------------
    def __find_in_dirpath(
            self,
            type_0files_1dirs: int,
            dirpath: Union[str, pathlib.Path] = None,
            return_0obj_1name: int = 0,  # TRY NOT TO USE STEMS!!!!
            wmask: Union[None, str, list] = None,
            nested: bool = False,
    ) -> list[Union[str, pathlib.Path]]:
        """
        list all variants. Repeated items not shown! order is preserved!
        """
        wmask = wmask or "*"
        wmask = UFU.sequence_make_ensured_if_not(wmask)

        dirpath = self.dirpath_get_active(dirpath)
        result = []

        for mask in wmask:
            mask = mask if not nested else f"**/{mask}"
            for path_obj in dirpath.glob(mask):
                if (type_0files_1dirs == 0 and path_obj.is_file()) or (type_0files_1dirs == 1 and path_obj.is_dir()):
                    if path_obj not in result:
                        result.append(path_obj)

        # FINISH
        if return_0obj_1name == 1:
            result = [path_obj.name for path_obj in result]

        print(f"{result=}")
        return result

    def files_find_in_dirpath(self, **kwargs):
        return self.__find_in_dirpath(type_0files_1dirs=0, **kwargs)

    def dirs_find_in_dirpath(self, **kwargs):
        return self.__find_in_dirpath(type_0files_1dirs=1, **kwargs)

    # DELETE ----------------------------------------------------------------------------------------------------------
    def files_find_and_delete_older(
            self,
            point: Union[None, int, float, datetime.datetime] = None,
            **kwargs
    ) -> None:
        files = self.files_find_in_dirpath(**kwargs)
        return self.files_delete_older(files=files, point=point)

    def files_delete_older(
            self,
            files: list[Union[str, pathlib.Path]],
            point: Union[None, int, float, datetime.datetime] = None
    ) -> None:
        # INPUT
        if isinstance(point, (datetime.datetime)):
            point = point.timestamp()
        if not isinstance(point, (type(None), int, float)):
            raise Exception

        # WORK
        for filepath in files:
            filepath = pathlib.Path(filepath)
            if not filepath.is_file():
                continue
            if not point or filepath.stat().st_mtime < point:
                filepath.unlink()

    # TODO: NOT WORKING!!!!! FINISH!!!! cant delete by access reason!!!
    def dirs_delete_if_blank(
            self,
            dirpath: Union[str, pathlib.Path],
            nested: bool = False
    ):
        dirs = self.dirs_find_in_dirpath(dirpath=dirpath, nested=nested)
        for dirpath in dirs:
            try:
                dirpath.rmdir()
            except:
                pass


# =====================================================================================================================
class File(Dir):
    """
    BASE CLASS FOR WORKING WITH FILES! and selecting only one!
    if you need work only with path objects in FileSystem (list_dir for example) without exactly opening files
    use it directly or create special class.
    In other cases with special file types use other special classes inherited from this - Json/Log

    ATTENTION:
        1. DONT USE FILES READ/WRITE WITHOUT SELECTING!!!
            if you creating instance for working with exact file - dont read/write another file without selecting new one!!!
            all methods who get filepath-like parameter - will and must use selecting it!!!
    """
    FILEPATH_BACKUP: bool = None     # used right before dump

    __filepath: pathlib.Path = None

    @property
    def FILEPATH(self) -> pathlib.Path | None:
        return self.__filepath

    @FILEPATH.setter
    def FILEPATH(self, value) -> None:
        self.__filepath = value
        # todo: dirpath

    # =================================================================================================================
    def __init__(self, filepath: Union[None, str, pathlib.Path] = None, **kwargs):
        super().__init__(**kwargs)

        if filepath is not None:
            self.FILEPATH = filepath

        if filepath is not None:
            self.FILEPATH = pathlib.Path(self.FILEPATH)

    def get_active__filepath(
            self,
            filepath: Union[None, str, pathlib.Path] = None,
    ) -> Optional[pathlib.Path]:
        """
        used always get final pathlib (from instanse or specified param)
        """
        if filepath is None:
            filepath = self.FILEPATH
        else:
            filepath = pathlib.Path(filepath)

        if filepath is None:
            msg = f"blank {filepath=}"
            print(msg)
        return filepath

    # FINISH ==========================================================================================================
    def try_find_wo_extension(self):
        """
        GOAL
        ----
        same as attrs caseInsensitive for classes but for obvious finding files
        it could mention with extension or not
        """
        pass
        # TODO: finish

    # FILEPATH ========================================================================================================
    def filepath_check_exists(self, filepath: pathlib.Path = None) -> Optional[bool]:
        filepath = self.get_active__filepath(filepath)
        if filepath:
            return filepath.exists()

    def filepath_get_by_name(
            self,
            name: str,
            dirpath: Union[None, str, pathlib.Path] = None,
            only_if_existed: bool = False
    ) -> Optional[pathlib.Path]:  # never add wildcard or short name WoExt!!!
        if not name:
            msg = f"no {name=}"
            print(msg)
            return

        dirpath = self.dirpath_get_active(dirpath)
        filepath = dirpath.joinpath(name)
        if not only_if_existed or (only_if_existed and filepath.exists()):
            return filepath

    def filepath_set(self, filepath: Union[str, pathlib.Path], only_if_existed: bool = False) -> Optional[bool]:
        if not filepath:
            msg = f"blank {filepath=}"
            print(msg)
            return

        filepath = pathlib.Path(filepath)

        if only_if_existed and not filepath.exists():
            msg = f"file not exists {filepath=}"
            print(msg)
            return

        self.FILEPATH = filepath
        return True

    def filepath_set_by_name(
            self,
            name: str,
            dirpath: Union[None, str, pathlib.Path] = None,
            only_if_existed: bool = False
    ) -> Optional[bool]:    # never add wildcard or short name WoExt!!!
        filepath = self.filepath_get_by_name(name=name, dirpath=dirpath, only_if_existed=only_if_existed)
        if filepath:
            return self.filepath_set(filepath=filepath, only_if_existed=only_if_existed)

    def filepath_get_with_new_stem(
            self,
            filepath: Union[None, str, pathlib.Path] = None,
            start_suffix: Optional[str] = None,
            preend_suffix: Optional[str] = None,
            end_suffix: Optional[str] = None
    ) -> Optional[pathlib.Path]:
        """
        for backup actually!
        """
        filepath = self.get_active__filepath(filepath)
        if not filepath:
            msg = f"not exists {filepath=}"
            print(msg)
            return

        start_suffix = start_suffix or ""
        preend_suffix = preend_suffix or ""
        end_suffix = end_suffix or ""

        filepath = filepath.parent.joinpath(f"{start_suffix}{filepath.stem}{preend_suffix}{end_suffix}{filepath.suffix}")
        return filepath

    # BACKUPS ---------------------------------------------------------------------------------------------------------
    def filepath_backup_make(
            self,
            filepath: Union[None, str, pathlib.Path] = None,
            dirpath: Union[None, str, pathlib.Path] = None,
            backup: Optional[bool] = None,
    ) -> Optional[bool]:
        # DECIDE --------------------------------
        backup = backup if backup is not None else self.FILEPATH_BACKUP
        if not backup:
            return True

        # SOURCE --------------------------------
        source = self.get_active__filepath(filepath)
        if not source.exists():
            msg = f"not exists {source=}"
            print(msg)
            return

        # DESTINATION --------------------------------
        # be careful to change this code!
        if filepath is not None and dirpath is None:
            destination = source.parent
        else:
            destination = self.dirpath_get_active(dirpath)
        destination = destination.joinpath(source.name)

        # suffix --------------------------------
        end_suffix = UFU.datetime_get_datetime_str()
        backup_filepath = self.filepath_get_with_new_stem(destination, start_suffix="-", preend_suffix="_", end_suffix=end_suffix)
        try:
            shutil.copy(source, backup_filepath)
            return True
        except:
            pass

    def file_backups_get_wildmask(self, filepath: Union[None, str, pathlib.Path] = None) -> str:
        filepath = self.get_active__filepath(filepath)
        wmask = f"*{filepath.stem}*{filepath.suffix}"
        return wmask

    def filepath_backups_get(
            self,
            filepath: Optional[pathlib.Path] = None,
            dirpath: Optional[pathlib.Path] = None,
            nested: bool = True
    ) -> list[pathlib.Path]:
        """
        find all backup files nearby
        """
        wmask = self.file_backups_get_wildmask(filepath)
        result = self.files_find_in_dirpath(dirpath=dirpath, wmask=[wmask], nested=nested)
        result = sorted(result, key=lambda obj: obj.stat().st_mtime, reverse=True)

        # exclude original data file
        if self.FILEPATH in result:
            result.remove(self.FILEPATH)

        return result

    def file_backups_delete__except_last_count(self, count: int = 15, filepath: Optional[pathlib.Path] = None, dirpath: Optional[pathlib.Path] = None) -> None:
        """
        delete old backups
        """
        filepath_to_delete_list = self.filepath_backups_get(filepath=filepath, dirpath=dirpath)
        if count:
            filepath_to_delete_list = filepath_to_delete_list[count:]

        for filepath in filepath_to_delete_list:
            filepath.unlink()

    def file_backups_delete__older(
            self,
            point: Union[int, float, datetime.datetime],
            filepath: Optional[pathlib.Path] = None,
            dirpath: Optional[pathlib.Path] = None) -> None:
        """
        delete old backups
        """
        filepath_to_delete_list = self.filepath_backups_get(filepath=filepath, dirpath=dirpath)
        return self.files_delete_older(point=point, files=filepath_to_delete_list)

    # READ/WRITE ======================================================================================================
    # READ ---------------------------------
    def read__text(self, filepath=None) -> Optional[str]:
        filepath = self.get_active__filepath(filepath)
        if filepath.exists() and filepath.is_file():
            return filepath.read_text(encoding="utf-8")

    def read__bytes(self, filepath=None) -> Optional[bytes]:
        filepath = self.get_active__filepath(filepath)
        if filepath.exists() and filepath.is_file():
            return filepath.read_bytes()

    # WRITE ---------------------------------
    def write__text(self, text: str, filepath=None) -> Optional[int]:
        filepath = self.get_active__filepath(filepath)
        if filepath:
            self.dirpath_ensure(self.FILEPATH.parent)
            return filepath.write_text(data=text, encoding="utf-8")

    def write__bytes(self, data: bytes, filepath=None) -> Optional[int]:
        filepath = self.get_active__filepath(filepath)
        if filepath:
            self.dirpath_ensure(self.FILEPATH.parent)
            return filepath.write_bytes(data=data)


# =====================================================================================================================
# FILE ----------------------------------------------------------------------------------------------------------------
def file_wait_while_exists(path, timeout=5):
    """ Waits while file exists for 'timeout'.
    """
    path = pathlib.Path(path)

    for i in range(timeout):
        if not path.exists():
            return True
        time.sleep(1)
    return


def file_save_data(data=None, filename="FILE.DUMP", dirpath=None, append=False):
    # INPUTS ------------------------------------------------
    if dirpath:
        dirpath = pathlib.Path(dirpath)
    else:
        dirpath = CONSTANTS.DIRPATH_TEMP

    dirpath.mkdir(parents=True, exist_ok=True)

    filepath = dirpath.joinpath(filename)

    if append:
        _type = "a"
    else:
        _type = "w"

    # WORK -------------------------------------------------
    with open(file=filepath, encoding="UTF-8", mode=_type) as _fo:
        _fo.write(data)

    return True


# PATH ----------------------------------------------------------------------------------------------------------------
def path_dirs_create_all_pathlib_links_from_module_link(source):
    """
    specially create for creating all pathlib-tree-links from CONSTANTS (module)!
    if pathlib link is file - create tree-dir to it!
    desined for module-link but it can be work for any object (but not actually usefull)!

    :param source:
    :return:
    """
    if not type_is_1_module_link(source):
        msg = f"type incorrect {source=} need MODULE"
        print(msg)
        return

    elements_dict = obj_elements_get_dict_all(source)
    if elements_dict:
        for element_name, element_obj in elements_dict.items():
            if isinstance(element_obj, pathlib.Path):
                if len(element_obj.drive) > 2:
                    # detected LAN path
                    continue
                if not element_obj.drive:
                    msg = f"detected not absolute path {element_obj=} need to make it absolute!"
                    print(msg)
                    continue

                if not element_obj.exists():
                    if "." in element_obj.name:
                        dirpath = element_obj.parent
                    else:
                        dirpath = element_obj

                    dirpath.mkdir(parents=True, exist_ok=True)
                    msg = f"makedirs {dirpath}"
                    print(msg)

    return True


def path_cwd_check_run_correctly(filename, path_cwd, raise_if_false=True):
    """show if you correctly starting your project!

    используется только в корневом файле проекта, который запускает пользователь!
    причина появления функции - пользователь может открыть терминал CMD и закинуть в него корневой файл проекта
    проект может запуститься НО корневая директория будет считаться корневой директорией терминала а не директорией проекта!!
    от этого все внутренние ссылки в проекте на текущий каталог будут неверными и ниодного файла/каталога не будет видно!

    RECOMMENDED USAGE!!!!
        import pathlib
        path_cwd_check_run_correctly(__file__, pathlib.Path.cwd())    # PLACE ONLY IN ROOT(__MAIN__) FILE!!!

    :param filename: recommended __file__
    :param path_cwd: recommended pass pathlib.Path.cwd() but you can use str or else
    """
    # todo: in future you may can work with stack! use __name_/__main__ ets...

    dirpath = pathlib.Path(filename).parent
    path_cwd = pathlib.Path(path_cwd)
    result = dirpath == path_cwd
    if not result:
        msg = f"""
            НЕВЕРНЫЙ КОРНЕВОЙ ПУТЬ (CWD) ЗАПУСКА ПРОГРАММЫ\n
            ПОСЛЕДСТВИЯ - программа не увидит папки и файлы проекта\n
            скорее всего запуск прозошел в терминале CMD\n
            фактическое расположение файла=[{dirpath=}]
            определен текущий каталог программой=[{path_cwd=}]

            для корректного запуска - в используемом терминале перейдите из [path_cwd] в [path_file]
        """
        print(msg)
        if raise_if_false:
            raise Exception(msg)

    return result


# =====================================================================================================================

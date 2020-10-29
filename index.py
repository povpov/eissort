import os
import zipfile

BASE_DIR = ""
TYPE_FOR_SAVE = [
    'epClarificationDoc',
    'fcsNotificationEA44',
    'fcsNotificationEA615',
    'fcsNotificationCancel',
    'fcsPlacementResult',
    'fcsNotificationZK504',
    'fcsNotificationOK504',
    'fcsNotificationOKU504',
    'fcsNotificationPO615',
    'fcsNotificationZP504',
    'epProlongationCancelEZK',
    'epProlongationCancelEOKOU',
    'fcsNotificationLotCancel',
    'epProlongationEOK',
    'epProlongationEOKOU',
    'epProlongationEZK',
    'fcsNotificationCancelFailure',
    'fcsContractSign',
    'fcs_notificationEFDateChange',
    'fcsNotificationOrgChange',
    'fcsNotificationOKD504',
]
TYPE_FOR_DELETE = [
    'fcsNotificationINM111',
    'fcsNotificationZA44',
    'epClarificationResult',
    'fcsNotificationZKK44',
    'fcsNotificationZK44',
    'fcsNotificationZKKU44',
    'fcsNotificationOK44',
]

NEW = 'new'
os.chdir(os.path.join(BASE_DIR, NEW))


def file_move(filename, filetype):
    # пеемещение файла
    try:
        os.rename(filename, os.path.join(BASE_DIR, filetype, filename))
    except FileExistsError:
        print("дубль:", filename)
        os.remove(filename)


if os.listdir():
    print("Все папки и файлы:", os.listdir())
    for dirpath, dirnames, filenames in os.walk("."):
        print("dirpath:", dirpath)

        for filename in filenames:
            filetype = filename.split('_')[0]
            extention = filename[-3:]
            filepath = os.path.join(dirpath, filename)
            print("Файл:", os.path.join(dirpath, filename))

            # Уделение файлов с ЭП и дублей
            if extention == 'sig' or filetype in TYPE_FOR_DELETE:
                os.remove(filename)
                continue

            if extention == 'zip':
                filezip = zipfile.ZipFile(os.getcwd()+f'/{filename}')
                filezip.extractall()
                filezip.close()

                file_move(filename, 'zip')
                continue

            # пеемещение файла
            if extention == "xml":
                if filename.find("fcs_notificationEFDateChange") == 0:
                    file_move(filename, "fcs_notificationEFDateChange")
                    continue

                if filetype in TYPE_FOR_SAVE:
                    file_move(filename, filetype)

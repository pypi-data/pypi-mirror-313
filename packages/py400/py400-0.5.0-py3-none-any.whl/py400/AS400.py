import sys
from itoolkit import (
    iToolKit,
    iCmd5250,
    iPgm,
    iData,
    iDS,
    iSqlPrepare,
    iSqlParm,
    iSqlExecute,
    iSqlFetch,
    iSqlFree,
)
from itoolkit.transport import DatabaseTransport
import pyodbc
from pprint import pprint
from datetime import datetime, timedelta

"""
C types          RPG types                     XMLSERVICE types                                   SQL types
===============  ============================  ================================================   =========
int8/byte        D myint8    3i 0              <data type='3i0'/>                                 TINYINT   (unsupported DB2)
int16/short      D myint16   5i 0 (4b 0)       <data type='5i0'/>                                 SMALLINT
int32/int        D myint32  10i 0 (9b 0)       <data type='10i0'/>                                INTEGER
int64/longlong   D myint64  20i 0              <data type='20i0'/>                                BIGINT
uint8/ubyte      D myuint8   3u 0              <data type='3u0'/>
uint16/ushort    D myuint16  5u 0              <data type='5u0'/>
uint32/uint      D myuint32 10u 0              <data type='10u0'/>
uint64/ulonglong D myuint64 20u 0              <data type='20u0'/>
char             D mychar   32a                <data type='32a'/>                                 CHAR(32)
varchar2         D myvchar2 32a   varying      <data type='32a' varying='on'/>                    VARCHAR(32)
varchar4         D myvchar4 32a   varying(4)   <data type='32a' varying='4'/>
packed           D mydec    12p 2              <data type='12p2'/>                                DECIMAL(12,2)
zoned            D myzone   12s 2              <data type='12s2'/>                                NUMERIC(12,2)
float            D myfloat   4f                <data type='4f2'/>                                 FLOAT
real/double      D myreal    8f                <data type='8f4'/>                                 DOUBLE
binary           D mybin    (any)              <data type='9b'>F1F2F3</data>                      BINARY
hole (no out)    D myhole   (any)              <data type='40h'/>
boolean          D mybool    1n                <data type='4a'/>                                  CHAR(4)
time             D mytime     T   timfmt(*iso) <data type='8A'>09.45.29</data>                    TIME
timestamp        D mystamp    Z                <data type='26A'>2011-12-29-12.45.29.000000</data> TIMESTAMP
date             D mydate     D   datfmt(*iso) <data type='10A'>2009-05-11</data>                 DATE
"""


class CommitMode:
    """
    Copied from : https://gist.github.com/mbiette/6cfd5b2dc2624c094575
    """

    NONE = 0  # Commit immediate (*NONE)  --> QSQCLIPKGN
    CS = 1  # Read committed (*CS)        --> QSQCLIPKGS
    CHG = 2  # Read uncommitted (*CHG)    --> QSQCLIPKGC
    ALL = 3  # Repeatable read (*ALL)     --> QSQCLIPKGA
    RR = 4  # Serializable (*RR)          --> QSQCLIPKGL


class ConnectionType:
    """
    Copied from : https://gist.github.com/mbiette/6cfd5b2dc2624c094575
    """

    ReadWrite = 0  # Read/Write (all SQL statements allowed)
    ReadCall = 1  # Read/Call (SELECT and CALL statements allowed)
    Readonly = 2  # Read-only (SELECT statements only)


class AS400:
    count = 0

    def __init__(self, address, username, password):
        self.count += 1

        self.__address = address
        self.__username = username
        self.__password = password

        self.__CPUUsage = None
        self.__OSName = None
        self.__OSVersion = None
        self.__OSRelease = None
        self.__hostName = None
        self.__CPUSCount = None
        self.__configuredCPUS = None
        self.__configuredMemory = None
        self.__totalMemory = None

        self.connection = pyodbc.connect(
            f"""DRIVER=iSeries Access ODBC Driver;
                SYSTEM={self.__address};
                UID={self.__username};
                PWD={self.__password};
                TRANSLATE=1;
                CommitMode={CommitMode.NONE};
                ConnectionType={ConnectionType.ReadWrite};"""
        )

        self.itransport = DatabaseTransport(self.connection)
        self.itool = iToolKit()

        self.getSystemInformation()

    def __del__(self):
        self.count -= 1

    def getWRKSYSSTS(self):
        self.itool.add(iCmd5250("wrksyssts", "WRKSYSSTS"))
        self.itool.call(self.itransport)

        pprint(self.itool.dict_out("wrksyssts"))
        self.itool.clear()

    def getQWCRSSTS(
        self, resetInput: bool = False, format: str = "SSTS0220", debug: bool = False
    ):
        """search for QWCRSSTS on https://www.ibm.com/docs/en/i/7.4?topic=interfaces-api-finder"""
        if format == "SSTS0220":
            self.itool.add(
                iPgm("qwcrssts", "QWCRSSTS", {"error": "on" if debug else "fast"})
                .addParm(
                    iDS("qwcrssts", {"len": "sstlen"})
                    # Bytes available
                    .addData(iData("Avl", "10i0", ""))
                    # Bytes returned
                    .addData(iData("Ret", "10i0", ""))
                    # Current date and time
                    .addData(iData("CDT", "8b", ""))
                    # System name
                    .addData(iData("SN", "8A", ""))
                    # Elapsed time
                    .addData(iData("ET", "6A", ""))
                    # Restricted state flag
                    .addData(iData("RF", "1A", ""))
                    # Processor sharing attribute
                    .addData(iData("PSA", "1A", ""))
                    # % processing unit used
                    .addData(iData("PUU", "10i0", ""))
                    # Jobs in system
                    .addData(iData("JIS", "10i0", ""))
                    # Number of partitions
                    .addData(iData("NPA", "10i0", ""))
                    # Current processing capacity
                    .addData(iData("CPC", "10i0", ""))
                    # Number of processors
                    .addData(iData("NPR", "10i0", ""))
                    # Active jobs in system
                    .addData(iData("AJS", "10i0", ""))
                    # Active threads in system
                    .addData(iData("ATS", "10i0", ""))
                    # Maximum jobs in system
                    .addData(iData("MJS", "10i0", ""))
                )
                .addParm(iData("rcvlen", "10i0", "", {"setlen": "sstlen"}))
                .addParm(iData("fmtnam", "8a", format))
                .addParm(iData("rstipt", "10a", "*YES " if resetInput else "*NO "))
                .addParm(
                    iDS("ERRC0100_T", {"len": "errlen"})
                    .addData(iData("errRet", "10i0", ""))
                    .addData(iData("errAvl", "10i0", ""))
                    .addData(iData("errExp", "7a", "", {"setlen": "errlen"}))
                    .addData(iData("errRsv", "1a", ""))
                )
            )
        elif format == "SSTS0200":
            self.itool.add(
                iPgm("qwcrssts", "QWCRSSTS", {"error": "on" if debug else "fast"})
                .addParm(
                    iDS("qwcrssts", {"len": "sstlen"})
                    .addData(iData("Avl", "10i0", ""))  # Bytes available
                    .addData(iData("Ret", "10i0", ""))  # Bytes returned
                    # Current date and time
                    .addData(iData("CDT", "8b", ""))
                    # System name
                    .addData(iData("SN", "8A", ""))
                    # Elapsed time
                    .addData(iData("ET", "6A", ""))
                    # Restricted state flag
                    .addData(iData("RSF", "1A", ""))
                    # Reserved
                    .addData(iData("R1", "1A", ""))
                    # % processing unit used
                    .addData(iData("PUU", "10i0", ""))
                    # Jobs in system
                    .addData(iData("JIS", "10i0", ""))
                    # % permanent addresses
                    .addData(iData("NPA", "10i0", ""))
                    # % temporary addresses
                    .addData(iData("NTA", "10i0", ""))
                    # System ASP
                    .addData(iData("SASP", "10i0", ""))
                    # % system ASP used
                    .addData(iData("NASP", "10i0", ""))
                    # Total auxiliary storage
                    .addData(iData("TAS", "10i0", ""))
                    # Current unprotected storage used
                    .addData(iData("CUSU", "10i0", ""))
                    # Maximum unprotected storage used
                    .addData(iData("MUSU", "10i0", ""))
                    # % DB capability
                    .addData(iData("DBC", "10i0", ""))
                    # Main storage size
                    .addData(iData("MSZ", "10i0", ""))
                    # Number of partitions
                    .addData(iData("NP", "10i0", ""))
                    # Partition identifier
                    .addData(iData("PI", "10i0", ""))
                    # Reserved
                    .addData(iData("R2", "10i0", ""))
                    # Current processing capacity
                    .addData(iData("CPC", "10i0", ""))
                    # Processor sharing attribute
                    .addData(iData("PSA", "1A", ""))
                    # Reserved
                    .addData(iData("PSA", "3A", ""))
                    # Number of processors
                    .addData(iData("NPR", "10i0", ""))
                    # Active jobs in system
                    .addData(iData("AJS", "10i0", ""))
                    # Active threads in system
                    .addData(iData("ATS", "10i0", ""))
                    # Maximum jobs in system
                    .addData(iData("MJS", "10i0", ""))
                    # % temporary 256MB segments used
                    .addData(iData("NTMBSU", "10i0", ""))
                    # % temporary 4GB segments used
                    .addData(iData("NTGBSU", "10i0", ""))
                    # % permanent 256MB segments used
                    .addData(iData("NPMBSU", "10i0", ""))
                    # % permanent 4GB segments used
                    .addData(iData("NPGBSU", "10i0", ""))
                    # % current interactive performance
                    .addData(iData("NCIP", "10i0", ""))
                    # % uncapped CPU capacity used
                    .addData(iData("NUCPUCU", "10i0", ""))
                    # % shared processor pool used
                    .addData(iData("NSPPU", "10i0", ""))
                    # Main storage size(long)
                    .addData(iData("MSS", "20u0", ""))
                )
                .addParm(iData("rcvlen", "10i0", "", {"setlen": "sstlen"}))
                .addParm(iData("fmtnam", "8a", format))
                .addParm(iData("rstipt", "10a", "*YES " if resetInput else "*NO "))
                .addParm(
                    iDS("ERRC0100_T", {"len": "errlen"})
                    .addData(iData("errRet", "10i0", ""))
                    .addData(iData("errAvl", "10i0", ""))
                    .addData(iData("errExp", "7a", "", {"setlen": "errlen"}))
                    .addData(iData("errRsv", "1a", ""))
                )
            )

        self.itool.call(self.itransport)

        qwcrssts = self.itool.dict_out("qwcrssts")
        self.itool.clear()
        if "success" in qwcrssts:
            qwcrssts_result = qwcrssts["qwcrssts"]
            if debug:
                print(qwcrssts["success"])
                print("Length of receiver variable      : " + qwcrssts["rcvlen"])
                print("Format name                      : " + qwcrssts["fmtnam"])
                print("Reset status statistics          : " + qwcrssts["rstipt"])
                print("-" * 10)
                print("\tBytes available                : " + qwcrssts_result["Avl"])
                print("\tBytes returned                 : " + qwcrssts_result["Ret"])
                print(
                    "\tCurrent date and time          : "
                    + str(self.convertDTStoTimestamp(qwcrssts_result["CDT"]))
                )
                print("\tSystem name                    : " + qwcrssts_result["SN"])
                print("\tElapsed time                   : " + qwcrssts_result["ET"])
                print("\tRestricted state flag          : " + qwcrssts_result["RF"])
                print("\tProcessor sharing attribute    : " + qwcrssts_result["PSA"])
                print("\t% processing unit used         : " + qwcrssts_result["PUU"])
                print("\tJobs in system                 : " + qwcrssts_result["JIS"])
                print("\tNumber of partitions           : " + qwcrssts_result["NPA"])
                print("\tCurrent processing capacity    : " + qwcrssts_result["CPC"])
                print("\tNumber of processors           : " + qwcrssts_result["NPR"])
                print("\tActive jobs in system          : " + qwcrssts_result["AJS"])
                print("\tActive threads in system       : " + qwcrssts_result["ATS"])
                print("\tMaximum jobs in system         : " + qwcrssts_result["MJS"])
            else:
                self.__CPUUsage = int(qwcrssts_result["PUU"]) / 10
                if format == "SSTS0200":
                    self.__ASPUsage = float(qwcrssts_result["NASP"]) / 10000
                    self.__activeJobsInSystem = int(qwcrssts_result["JIS"])
                    self.__maximumJobsInSystem = int(qwcrssts_result["MJS"])
                self.__cpuQuantity = qwcrssts_result["NPR"]
                self.__currentProcessingCapacity = qwcrssts_result["CPC"]

                return qwcrssts["qwcrssts"]
        else:
            pprint(qwcrssts)

    def getListOfSpoolFiles(
        self,
        userName: str = "*ALL",
        jobName: str = "*ALL",
        formType: str = "EMail!ERR",
        startDate: datetime = datetime.combine(datetime.today(), datetime.min.time()),
        endDate: datetime = datetime.now(),
        debug: bool = False,
    ):
        self.itool.add(
            iSqlPrepare(
                "listOfSpoolFiles",
                f"""SELECT * FROM TABLE(QSYS2.SPOOLED_FILE_INFO(USER_NAME => '{userName}', JOB_NAME => '{jobName}', FORM_TYPE => '{formType}', STARTING_TIMESTAMP => '{startDate.strftime("%Y-%m-%d-%H.%M.%S")}', ENDING_TIMESTAMP => '{endDate.strftime("%Y-%m-%d-%H.%M.%S")}'));""",
                {"error": "on" if debug else "fast"},
            )
        )

        self.itool.add(iSqlExecute("exec", {"error": "on" if debug else "fast"}))

        self.itool.add(iSqlFetch("fetch", {"error": "on" if debug else "fast"}))
        self.itool.add(iSqlFree("free", {"error": "on" if debug else "fast"}))

        self.itool.call(self.itransport)

        requestResult = self.itool.dict_out("fetch")
        self.itool.clear()

        if "error" in requestResult:
            print(requestResult["error"], file=sys.stderr, flush=True)
            raise Exception(requestResult["error"])
        else:
            return requestResult["row"]

    def getSpoolFileData(self, qualifiedJobName : str, spoolFileName : str = "", debug : bool = False):
        self.itool.add(
            iSqlPrepare(
                "listOfSpoolFiles",
                f"""SELECT * FROM TABLE(SYSTOOLS.SPOOLED_FILE_DATA(
                             JOB_NAME          =>'{qualifiedJobName}'
                             {f", SPOOLED_FILE_NAME =>'{spoolFileName}'" if spoolFileName else ""})) 
                    ORDER BY ORDINAL_POSITION;""",
                {"error": "on" if debug else "fast"},
            )
        )

        self.itool.add(iSqlExecute("exec", {"error": "on" if debug else "fast"}))

        self.itool.add(iSqlFetch("fetch", {"error": "on" if debug else "fast"}))
        self.itool.add(iSqlFree("free", {"error": "on" if debug else "fast"}))

        self.itool.call(self.itransport)

        requestResult = self.itool.dict_out("fetch")
        self.itool.clear()

        if "error" in requestResult:
            print(requestResult["error"], file=sys.stderr, flush=True)
            raise Exception(requestResult["error"])
        else:
            finalResult = ""
            for row in requestResult["row"]:
                finalResult += row["SPOOLED_DATA"] + '\n'
            return finalResult
    
    def getQWCCVTDT(
        self,
        inputVar: str,
        inputFormat: str = "*DTS",
        outputFormat: str = "*YYMD",
        debug: bool = False,
    ):
        """
        The DTS format is a representation on 8 Bytes of the microseconds elapsed since "1928-08-23 12:03:06.315".
        Each increments represents a value from 8 microseconds.
        This format will stop working on "2071-05-10 11:56:53.685".
        """

        iptVarCType = "17A"
        optVarCType = "17A"

        if inputFormat == "*DTS":
            iptVarCType = "8b"
        elif inputFormat == "*YYMD":
            iptVarCType = "17A"
        elif inputFormat == "*CURRENT":
            iptVarCType = "17A"

        if outputFormat == "*DTS":
            optVarCType = "8b"
        elif outputFormat == "*YYMD":
            optVarCType = "17A"

        self.itool.add(
            iPgm("qwccvtdt", "QWCCVTDT", {"error": "on" if debug else "fast"})
            .addParm(iData("iptfrm", "10A", inputFormat))
            .addParm(iData("iptVarC", iptVarCType, inputVar))
            .addParm(iData("optfrm", "10A", outputFormat))
            .addParm(iData("optVarC", optVarCType))
            .addParm(
                iDS("ERRC0100_t", {"len": "errlen"})
                .addData(iData("errRet", "10i0", ""))
                .addData(iData("errAvl", "10i0", ""))
                .addData(iData("errExp", "7A", "", {"setlen": "errlen"}))
                .addData(iData("errRsv", "1A", ""))
            )
        )
        self.itool.call(self.itransport)

        qwccvtdt = self.itool.dict_out("qwccvtdt")
        self.itool.clear()

        if "success" in qwccvtdt:
            if outputFormat == "*YYMD":
                return datetime.strptime(qwccvtdt["optVarC"], "%Y%m%d%H%M%S%f")
            else:
                return self.convertDTStoTimestamp(qwccvtdt["optVarC"])
        else:
            pprint(qwccvtdt)

    def convertDTStoTimestamp(self, DTS: str) -> datetime:
        DTS = int(DTS[0:13], 16)

        return datetime(1928, 8, 23, 12, 3, 6, 315000) + timedelta(microseconds=DTS)

    def robotTimestampToDateTime(self, timestamp: str) -> datetime:
        return datetime.strptime(timestamp[1:], "%y%m%d%H%M%S")

    def robotDateToDateTime(self, date: str) -> datetime:
        return datetime.strptime(date[1:], "%y%m%d")

    def robotTimeToDateTime(self, time: str) -> datetime:
        return datetime.strptime(time, "%H%M%S")

    def dateTimeToRobotTimestamp(self, timestamp: datetime) -> str:
        years = (timestamp.year - 1900) // 100
        return str(years) + timestamp.strftime("%y%m%d%H%M%S")

    def dateTimeToRobotDate(self, timestamp: datetime) -> str:
        years = (timestamp.year - 1900) // 100
        return years + timestamp.strftime("%y%m%d")

    def dateTimeToRobotTime(self, timestamp: datetime) -> str:
        return timestamp.strftime("%H%M%S")

    def getCompletedAndFailedJobs(self, overDays: int = 0, overHours: int = 12):
        endDate = datetime.now()
        self.itool.add(
            iSqlPrepare(
                "SAUVSPOOLprep",
                """
SELECT MSG.JOB_NAME,
    MSG.ROBOT_JOB_NUMBER,
    MSG.JOB_STATUS,
    MSG.OS_JOB_END_DATE,
    MSG.OS_JOB_END_TIME,
    MSG.TIME_STAMP,
    ROB.ROBOT_JOB_DESC,
    ROB.ROBOT_JOB_NOTES
FROM ROBOTLIB.RBTMSG AS MSG
    JOIN ROBOTLIB.RBTROB AS ROB
        ON MSG.ROBOT_JOB_NUMBER = ROB.ROBOT_JOB_NUMBER
WHERE MSG.JOB_STATUS IN ('T', 'C')
    AND (MSG.OS_JOB_END_DATE * 1000000) + MSG.OS_JOB_END_TIME >= ?
    AND (MSG.OS_JOB_END_DATE * 1000000) + MSG.OS_JOB_END_TIME <= ?
    AND MSG.JOB_NAME NOT LIKE 'ROBOT%'
    AND MSG.OS_JOB_USER <> 'RBTUSER'
    AND MSG.OS_JOB_USER <> 'RBTADMIN'
ORDER BY JOB_STATUS DESC,
        TIME_STAMP DESC
""",
            )
        )
        self.itool.add(
            iSqlExecute("exec")
            .addParm(
                iSqlParm(
                    "beginDate",
                    self.dateTimeToRobotTimestamp(
                        endDate + timedelta(days=overDays * -1, hours=overHours * -1)
                    ),
                )
            )
            .addParm(iSqlParm("endDate", self.dateTimeToRobotTimestamp(endDate)))
        )

        self.itool.add(iSqlFetch("fetch"))
        self.itool.add(iSqlFree("free"))

        self.itool.call(self.itransport)

        requestResult = self.itool.dict_out("fetch")
        self.itool.clear()

        result = []
        failedJobsNumbers = []

        if "error" in requestResult:
            print(requestResult["error"], file=sys.stderr, flush=True)
            raise Exception(requestResult["error"])
        else:
            for row in requestResult["row"]:
                if row["JOB_STATUS"] == "T":
                    if row["ROBOT_JOB_NUMBER"] in failedJobsNumbers:
                        for job in result:
                            if job["ROBOT_JOB_NUMBER"] == row["ROBOT_JOB_NUMBER"]:
                                job["failCount"] += 1
                    else:
                        failedJobsNumbers.append(row["ROBOT_JOB_NUMBER"])
                        result.append(
                            {
                                "JOB_NAME": row["JOB_NAME"],
                                "ROBOT_JOB_NUMBER": row["ROBOT_JOB_NUMBER"],
                                "ROBOT_JOB_DESC": row["ROBOT_JOB_DESC"],
                                "ROBOT_JOB_NOTES": row["ROBOT_JOB_NOTES"],
                                "OS_JOB_END_DATE": str(
                                    self.robotDateToDateTime(
                                        row["OS_JOB_END_DATE"]
                                    ).date()
                                )
                                + " "
                                + str(
                                    self.robotTimeToDateTime(
                                        row["OS_JOB_END_TIME"]
                                    ).time()
                                ),
                                "TIME_STAMP": self.robotTimestampToDateTime(
                                    row["TIME_STAMP"]
                                ),
                                "failCount": 1,
                                "reEndedSuccessfulyAt": None,
                            }
                        )

            for failedJob in result:
                for row in requestResult["row"]:
                    if (
                        failedJob["ROBOT_JOB_NUMBER"] == row["ROBOT_JOB_NUMBER"]
                        and failedJob["TIME_STAMP"] == row["TIME_STAMP"]
                    ):
                        failedJob["reEndedSuccessfulyAt"] = (
                            str(self.robotDateToDateTime(row["OS_JOB_END_DATE"]).date())
                            + " "
                            + str(
                                self.robotTimeToDateTime(row["OS_JOB_END_TIME"]).time()
                            )
                        )

            for failedJob in result:
                failedJob["TIME_STAMP"] = str(failedJob["TIME_STAMP"])

        self.itool.clear()
        return result

    def getUsers(self, limit: int = None, offset: int = 0, debug: bool = False):
        self.itool.add(
            iSqlPrepare(
                "UsersGet",
                f"""
SELECT *
    FROM (
            SELECT
                   CASE GROUP_ID_NUMBER
                       WHEN 0 THEN 'USER'
                       ELSE 'GROUP'
                   END AS PROFILE_TYPE,
                   AUTHORIZATION_NAME,
                   PREVIOUS_SIGNON,
                   SIGN_ON_ATTEMPTS_NOT_VALID,
                   STATUS,
                   NETSERVER_DISABLED,
                   PASSWORD_CHANGE_DATE,
                   NO_PASSWORD_INDICATOR,
                   PASSWORD_LEVEL_0_1,
                   PASSWORD_LEVEL_2_3,
                   PASSWORD_EXPIRATION_INTERVAL,
                   DATE_PASSWORD_EXPIRES,
                   DAYS_UNTIL_PASSWORD_EXPIRES,
                   SET_PASSWORD_TO_EXPIRE,
                   USER_CLASS_NAME,
                   SPECIAL_AUTHORITIES,
                   GROUP_PROFILE_NAME,
                   SUPPLEMENTAL_GROUP_COUNT,
                   SUPPLEMENTAL_GROUP_LIST,
                   OWNER,
                   GROUP_AUTHORITY,
                   ASSISTANCE_LEVEL,
                   CURRENT_LIBRARY_NAME,
                   INITIAL_MENU_NAME,
                   INITIAL_MENU_LIBRARY_NAME,
                   INITIAL_PROGRAM_NAME,
                   INITIAL_PROGRAM_LIBRARY_NAME,
                   LIMIT_CAPABILITIES,
                   CAST(TEXT_DESCRIPTION AS VARCHAR(50) CCSID 297)
                       AS TEXT_DESCRIPTION,
                   DISPLAY_SIGNON_INFORMATION,
                   LIMIT_DEVICE_SESSIONS,
                   KEYBOARD_BUFFERING,
                   MAXIMUM_ALLOWED_STORAGE,
                   STORAGE_USED,
                   HIGHEST_SCHEDULING_PRIORITY,
                   JOB_DESCRIPTION_NAME,
                   JOB_DESCRIPTION_LIBRARY_NAME,
                   ACCOUNTING_CODE,
                   MESSAGE_QUEUE_NAME,
                   MESSAGE_QUEUE_LIBRARY_NAME,
                   MESSAGE_QUEUE_DELIVERY_METHOD,
                   MESSAGE_QUEUE_SEVERITY,
                   OUTPUT_QUEUE_NAME,
                   OUTPUT_QUEUE_LIBRARY_NAME,
                   PRINT_DEVICE,
                   SPECIAL_ENVIRONMENT,
                   ATTENTION_KEY_HANDLING_PROGRAM_NAME,
                   ATTENTION_KEY_HANDLING_PROGRAM_LIBRARY_NAME,
                   LANGUAGE_ID,
                   COUNTRY_OR_REGION_ID,
                   CHARACTER_CODE_SET_ID,
                   USER_OPTIONS,
                   SORT_SEQUENCE_TABLE_NAME,
                   SORT_SEQUENCE_TABLE_LIBRARY_NAME,
                   OBJECT_AUDITING_VALUE,
                   USER_ACTION_AUDIT_LEVEL,
                   GROUP_AUTHORITY_TYPE,
                   USER_ID_NUMBER,
                   GROUP_ID_NUMBER,
                   LOCALE_JOB_ATTRIBUTES,
                   GROUP_MEMBER_INDICATOR,
                   DIGITAL_CERTIFICATE_INDICATOR,
                   CHARACTER_IDENTIFIER_CONTROL,
                   LOCAL_PASSWORD_MANAGEMENT,
                   BLOCK_PASSWORD_CHANGE,
                   USER_ENTITLEMENT_REQUIRED,
                   USER_EXPIRATION_INTERVAL,
                   USER_EXPIRATION_DATE,
                   USER_EXPIRATION_ACTION,
                   HOME_DIRECTORY,
                   LOCALE_PATH_NAME,
                   USER_DEFAULT_PASSWORD,
                   USER_OWNER,
                   USER_CREATOR,
                   SIZE,
                   CREATION_TIMESTAMP,
                   LAST_USED_TIMESTAMP,
                   DAYS_USED_COUNT,
                   LAST_RESET_TIMESTAMP,
                   AUTHORITY_COLLECTION_ACTIVE,
                   AUTHORITY_COLLECTION_REPOSITORY_EXISTS,
                   PASE_SHELL_PATH
                FROM QSYS2.USER_INFO
        )
        {f"LIMIT {limit} OFFSET {offset}" if limit else None}
""",
                {"error": "on" if debug else "fast"},
            )
        )

        self.itool.add(iSqlExecute("exec", {"error": "on" if debug else "fast"}))

        self.itool.add(iSqlFetch("fetch", {"error": "on" if debug else "fast"}))
        self.itool.add(iSqlFree("free", {"error": "on" if debug else "fast"}))

        self.itool.call(self.itransport)

        requestResult = self.itool.dict_out("fetch")
        self.itool.clear()

        if "error" in requestResult:
            print(requestResult["error"], file=sys.stderr, flush=True)
            raise Exception(requestResult["error"])
        else:
            return requestResult["row"]

    def getSystemInformation(self, debug: bool = False):
        self.itool.add(
            iSqlPrepare("getSysInfo", """SELECT * FROM SYSIBMADM.ENV_SYS_INFO""")
        )
        self.itool.add(iSqlExecute("exec"))

        self.itool.add(iSqlFetch("fetch"))
        self.itool.add(iSqlFree("free"))

        self.itool.call(self.itransport)

        queryResult = self.itool.dict_out("fetch")
        self.itool.clear()

        if "error" in queryResult:
            print(queryResult["error"])
            raise Exception(queryResult["error"])

        self.itool.clear()

        self.__OSName = queryResult["row"]["OS_NAME"]
        self.__OSVersion = queryResult["row"]["OS_VERSION"]
        self.__OSRelease = queryResult["row"]["OS_RELEASE"]
        self.__hostName = queryResult["row"]["HOST_NAME"]
        self.__CPUSCount = queryResult["row"]["TOTAL_CPUS"]
        self.__configuredCPUS = queryResult["row"]["CONFIGURED_CPUS"]
        self.__configuredMemory = queryResult["row"]["CONFIGURED_MEMORY"]
        self.__totalMemory = queryResult["row"]["TOTAL_MEMORY"]

        return queryResult["row"]

    def getCPUUsage(self):
        return round(self.__CPUUsage, 6)

    def getASPUsage(self):
        return round(self.__ASPUsage, 6)

    def getJOBUsage(self):
        return round((self.__activeJobsInSystem / self.__maximumJobsInSystem) * 100, 6)

    def getOSName(self):
        return self.__OSName

    def getOSVersion(self):
        return self.__OSVersion

    def getOSRelease(self):
        return self.__OSRelease

    def getHostName(self):
        return self.__hostName

    def getShortHostName(self):
        return self.__hostName[: self.__hostName.find(".")]

    def getCPUSCount(self):
        return self.__CPUSCount

    def getConfiguredCPUS(self):
        return self.__configuredCPUS

    def getConfiguredMemory(self):
        return self.__configuredMemory

    def getTotalMemory(self):
        return self.__totalMemory

    def _getColumnsNames(cursor):
        return [column[0] for column in cursor.description]
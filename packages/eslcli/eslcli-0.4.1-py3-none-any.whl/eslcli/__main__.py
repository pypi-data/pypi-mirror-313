import logging
import time
#FORMAT = '%(asctime)s+00:00 %(levelname)10s: %(message)-80s    (%(filename)s,%(funcName)s:%(lineno)s)'
FORMAT = '%(asctime)s+00:00 %(levelname)10s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.Formatter.converter = time.gmtime

import datetime
import argparse
import sys
import os
from rich.pretty import pprint as PP
import elasticsearch


parser = argparse.ArgumentParser(
    description="""UNOFFICIAL ELASTICSEARCH (R) (TM) LOGFILE TOOL
    """,
    prog="esl",
    epilog="""See EXAMPLES at the end for full invocations.

Supported (self-explanatory) environment variables:
    ESL_URL (default is "https://127.0.0.1:9200" if unset)
    ESL_APIKEY
    ESL_APIKEYFILE
    ESL_FINGERPRINT
    ESL_FINGERPRINTFILE

Supported TIMESPEC-FORMAT (Modes):
    (Always use only ONE time unit in statements: '1h' is ok, '1h30m' is not ok)
    
    MODE-1: 'back' (default)

        'back_3h'
            => last 3 hours, you can leave the prefix 'back_' since it is the default mode
    
    MODE-2: 'wasteback'
    
        'wasteback_1h_2h'
            => skip last hour and then search 2 hours back
    
    MODE-3: 'block'

        'block_2024-12-30_1h_2'
            => take Dec 30th, divide the day in 1h chunks and take chunk 2 form chunks 1..

        'block_._1h_2'
            => take today, ...
    
        take yesterday, ...
            => 'block_.._1h_2'

    MODE-4: 'single'

        'single_2024-12-30T12:30:00_30s'
            => take Dec 30th, from 12:30 UTC on 30 seconds

Example SSH Port Forward:
    ssh -L 127.0.0.1:9200:127.0.0.1:9200 ELK_HOST
""",
    formatter_class=argparse.RawDescriptionHelpFormatter
    )

parser.add_argument("-p", nargs=1, type=str, metavar="PREFIX", help="")
parser.add_argument("-t", nargs=1, type=str, metavar="TIMESPEC", help="")
parser.add_argument("-o", nargs=1, type=str, metavar="OUTFILE", help="")
parser.add_argument("-M", nargs=1, type=str, metavar="MODULE", help="")
parser.add_argument("-m", nargs=1, type=str, metavar="MATCH_PHRASE", help="")
parser.add_argument("-d", nargs=1, type=str, metavar="MATCH_PHRASE", help="document related")


args = parser.parse_args()

cfg_url = os.getenv("ESL_URL", "https://127.0.0.1:9200")

cfg_fingerprint = os.getenv("ESL_FINGERPRINT", "")
if cfg_fingerprint == "":
    cfg_fingerprintfile = os.getenv("ESL_FINGERPRINTFILE", "")
    if cfg_fingerprintfile != "":
        cfg_fingerprint = open(cfg_fingerprintfile, 'r').read().split("\n")[0].strip()

cfg_apikey = os.getenv("ESL_APIKEY", "")
if cfg_apikey == "":
    cfg_apikeyfile = os.getenv("ESL_APIKEYFILE", "")
    if cfg_apikeyfile != "":
        cfg_apikey = open(cfg_apikeyfile, 'r').read().split("\n")[0].strip()


def hotspec_seconds(src:str) -> int:
    res = 0
    # (s)econds
    if src.endswith("s"):
        res = int(src[:-1])
        return res
    # (m)inutes
    if src.endswith("m"):
        res = int(src[:-1])*60
        return res
    # (h)ours
    if src.endswith("h"):
        res = int(src[:-1])*3600
        return res
    # (d)ays
    if src.endswith("d"):
        res = int(src[:-1])*3600*24
        return res
    # (w)eeks
    if src.endswith("w"):
        res = int(src[:-1])*3600*24*7
        return res
    res = int(src)
    return res



argv_prefix = args.p[0] if args.p != None else None
argv_timespec = args.t[0] if args.t != None else None

if argv_timespec != None and not "_" in argv_timespec:
    argv_timespec = "back_" + argv_timespec


# if argv_timespec == None:
#     logging.error("Not running without timespec '-t'")
#     sys.exit(1)

if argv_prefix == None:
    logging.error("Not running without prefix '-p'")
    sys.exit(1)


timespec_cols = []
timespec_mode = "notime"

if argv_timespec != None:
    timespec_cols = argv_timespec.split("_")
    timespec_mode = timespec_cols[0]

if timespec_mode not in ["back", "wasteback", "block", "single", "notime"]:
    logging.error("Unknown timespec mode [%s]" % timespec_mode)
    sys.exit(1)


cfg = {
    'url': cfg_url,
    'apikey': cfg_apikey,
    'fingerprint': cfg_fingerprint
}

#PP(cfg)



def match_phrase_builder(k, v):
    res = {
        "match_phrase": {
            k: v
        }
    }
    return res

def term_builder(k, v):
    res = {
        "term": {
            k: v
        }
    }
    return res


def range_builder(gte_millis=-1, lt_millis=-1):
    res = {
        "range": {
            "@timestamp": {
                "format": "epoch_millis"
            }
        }
    }
    if gte_millis >= 0:
        res["range"]["@timestamp"]["gte"] = gte_millis
    if lt_millis >= 0:
        res["range"]["@timestamp"]["lt"] = lt_millis
    return res


# datetime instances for now and yesterday-now in utc
nowutc_dt = datetime.datetime.now(datetime.UTC)
yesterdayutc_dt = nowutc_dt - datetime.timedelta(days=1)

nowfile = nowutc_dt.isoformat().split("+")[0].split(".")[0]

# only YYYY-MM-DD strings for today and yetserday, utc
todayte = nowutc_dt.isoformat().split("T")[0]
yesterdayte = yesterdayutc_dt.isoformat().split("T")[0]

# init
the_filename = "log.txt"

the_filter = []

the_filter.append(match_phrase_builder(k="host.hostname", v=argv_prefix))


if args.M != None:
    the_filter.append(term_builder(k="event.module", v=args.M[0]))

if args.m != None:
    for mat in args.m:
        the_filter.append(match_phrase_builder(k="message", v=mat))

if args.d != None:
    for mat in args.d:
        the_filter.append(match_phrase_builder(k="document", v=mat))


# back_1h
if timespec_mode == "back":
    the_filename = "log_" + argv_prefix + "_" + timespec_mode + "_" + timespec_cols[1] + "_at_" + nowfile + ".txt" # todo include timespec
    back_seconds_value = hotspec_seconds(timespec_cols[1])
    gte_value = int(time.time()*1000)-int(1000*back_seconds_value)
    the_filter.append(range_builder(gte_millis=gte_value))

# wasteback_1h_2h (offset=1h logdur=2h)
if timespec_mode == "wasteback":
    the_filename = "log_" + argv_prefix + "_" + timespec_mode + "_" + timespec_cols[1] + "_" + timespec_cols[2] + "_at_" + nowfile + ".txt" # todo include timespec
    waste_seconds_value = hotspec_seconds(timespec_cols[1])
    back_seconds_value = hotspec_seconds(timespec_cols[2])
    gte_value = int(time.time()*1000)-int(1000*back_seconds_value)-int(1000*waste_seconds_value)
    lt_value = int(time.time()*1000)-int(1000*waste_seconds_value)
    the_filter.append(range_builder(gte_millis=gte_value, lt_millis=lt_value))

# block_2024-11-11_1h_8
# not implemented
if timespec_mode == "block":
    blockdayte = timespec_cols[1]
    if blockdayte == ".":
        blockdayte = todayte
    if blockdayte == "..":
        blockdayte = yesterdayte
    
    blocksize_spec = timespec_cols[2]
    blocksize_sec = hotspec_seconds(blocksize_spec)

    target_block = int(timespec_cols[3])

    block_from_dt = datetime.datetime.fromisoformat("%sT00:00:00+00:00" % blockdayte) + datetime.timedelta(seconds=blocksize_sec*(target_block-1))
    block_to_dt = block_from_dt + datetime.timedelta(seconds=blocksize_sec)

    the_filename = argv_prefix + "_" + timespec_mode + "_" + blockdayte + "_" + blocksize_spec + "_" + block_from_dt.strftime("%H:%M:%S") + "-" + block_to_dt.strftime("%H:%M:%S")

    gte = int(block_from_dt.timestamp())*1000
    lt = int(block_to_dt.timestamp())*1000
    the_filter.append(range_builder(gte_millis=gte, lt_millis=lt))

# not implemented
if timespec_mode == "single":
    the_filename = argv_prefix + "_" + timespec_mode
    the_filter.append(range_builder(gte_millis=0, lt_millis=0))



the_query = {
    "bool": {
        "must": {
            "match_all": {}
        },
        "filter": the_filter
    }
}

#PP(the_query)

#re-reset if necessary
if args.o is not None:
    the_filename = args.o[0]


logging.info("OUTPUT=%s" % the_filename)

logging.info("Sending request...")

es = elasticsearch.Elasticsearch(hosts=[cfg_url], api_key=cfg_apikey, ssl_assert_fingerprint=cfg_fingerprint)

x = es.search(
    index="filebeat-*",
    from_=0,
    size=10000,
    query=the_query
)

logging.info("Request done (total=%d)" % x['hits']['total']['value'])

if x['hits']['total']['value'] >= 10000:
    logging.warning("Search resulted in total hits of %d which will be truncated to 10000" % x['hits']['total']['value'])


unsorted_lines = []

byte_count = 0
with open(the_filename, 'w') as of:
    # order is not given
    for h in x['hits']['hits']:
        hit_orig = h["_source"]["event"]["original"]
        hit_host = h["_source"]["host"]["hostname"]
        hit_time = h["_source"]["@timestamp"]
        hit_mod = "no-module"
        if "module" in h["_source"]["event"].keys():
            hit_mod = h["_source"]["event"]["module"]
        hit_dataset = "no-dataset"
        if "dataset" in h["_source"]["event"].keys():
            hit_dataset = h["_source"]["event"]["dataset"]
        
        #oline = "%s %s %s %s %s\n" % (hit_time, hit_host, hit_mod, hit_dataset, hit_orig)
        #of.write(oline)

        tmp_dt_iso = datetime.datetime.fromisoformat(hit_time).replace(microsecond=0).isoformat()
        oline_retimed = "%s %s %s %s %s\n" % (tmp_dt_iso, hit_host, hit_mod, hit_dataset, hit_orig)
        byte_count += len(oline_retimed.encode(errors='replace'))
        unsorted_lines.append(oline_retimed)

logging.info("Sorting...")
unsorted_lines.sort()
logging.info("Sorting done")

logging.info("Writing...")
with open(the_filename, 'w') as of:
    for line in unsorted_lines:
        of.write(line)
logging.info("Writing done")

logging.info("Finished (%d KB)" % (int(byte_count/1024)))
sys.exit(0)

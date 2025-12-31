# sync-forced-2025
#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available

WAITFORIT_cmdname=${0##*/}

echoerr() { if [[ $WAITFORIT_QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

usage() {
    cat << USAGE >&2
Usage:
    $WAITFORIT_cmdname host:port [-s] [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
    -s | --strict               Only execute subcommand if the test succeeds
    -q | --quiet                Don't output any status messages
    -t TIMEOUT | --timeout=TIMEOUT
                                Timeout in seconds, zero for no timeout
    -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
}

wait_for() {
    local host="$WAITFORIT_HOST"
    local port="$WAITFORIT_PORT"
    local timeout="$WAITFORIT_TIMEOUT"
    local strict="$WAITFORIT_STRICT"
    local quiet="$WAITFORIT_QUIET"
    local start_time=$(date +%s)
    local end_time=$((start_time + timeout))
    local result=1

    while : ; do
        nc -z "$host" "$port" >/dev/null 2>&1
        result=$?
        if [[ $result -eq 0 ]]; then
            break
        fi
        if [[ $timeout -gt 0 ]]; then
            local now=$(date +%s)
            if [[ $now -ge $end_time ]]; then
                break
            fi
        fi
        sleep 1
    done
    return $result
}

# Parse arguments
WAITFORIT_HOST=""
WAITFORIT_PORT=""
WAITFORIT_TIMEOUT=15
WAITFORIT_STRICT=0
WAITFORIT_QUIET=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        *:* )
        WAITFORIT_HOST="${1%%:*}"
        WAITFORIT_PORT="${1##*:}"
        shift 1
        ;;
        -h)
        WAITFORIT_HOST="$2"
        shift 2
        ;;
        --host=*)
        WAITFORIT_HOST="${1#*=}"
        shift 1
        ;;
        -p)
        WAITFORIT_PORT="$2"
        shift 2
        ;;
        --port=*)
        WAITFORIT_PORT="${1#*=}"
        shift 1
        ;;
        -t)
        WAITFORIT_TIMEOUT="$2"
        shift 2
        ;;
        --timeout=*)
        WAITFORIT_TIMEOUT="${1#*=}"
        shift 1
        ;;
        -s|--strict)
        WAITFORIT_STRICT=1
        shift 1
        ;;
        -q|--quiet)
        WAITFORIT_QUIET=1
        shift 1
        ;;
        --)
        shift
        break
        ;;
        --help)
        usage
        exit 0
        ;;
        *)
        echoerr "Unknown argument: $1"
        usage
        exit 1
        ;;
    esac
    done

if [[ "$WAITFORIT_HOST" == "" || "$WAITFORIT_PORT" == "" ]]; then
    echoerr "Error: you need to provide a host and port to test."
    usage
    exit 1
fi

wait_for
result=$?

if [[ $WAITFORIT_STRICT -eq 1 ]]; then
    if [[ $result -ne 0 ]]; then
        echoerr "$WAITFORIT_cmdname: timeout occurred"
        exit $result
    fi
fi

shift $((OPTIND-1))

if [[ $# -gt 0 ]]; then
    exec "$@"
else
    exit $result
fi

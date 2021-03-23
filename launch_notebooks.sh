#!/usr/bin/env bash

## DESCRIPTION: Launch a Jupyter notebook server inside a Docker container for
#               running analysis notebooks. The container is set up
#               automatically the first time the script is run.

## AUTHOR: Paxton Fitzpatrick <Paxton.C.Fitzpatrick@Dartmouth.edu>

set -e

# default arg values
IMAGE_NAME="timecorr_paper"                  # name of image to build/use
CONTAINER_NAME="Timecorr_paper"              # name of container to create/start
declare -i LAUNCH_BROWSER=1                  # true by default
declare -i DETACH=0                          # false by default

# other configurables
# NOTE: changing these has no effect after image is built & container is created
declare -r DOCKERFILE_PATH="Dockerfile"      # relative path from repository root to Dockerfile
declare -r NOTEBOOKS_DIR="code/notebooks"    # relative path from repository root to notebooks folder
declare -ir CONTAINER_PORT=9999              # container port used to run notebook server and published to host
declare -ir LOCAL_PORT=9999                  # host port bound to container port and used to run notebooks in browser


########################################
#         CLI PARSING FUNCTIONS        #
########################################
parse_args() {
    while (( "$#" )); do
        case "$1" in
            -i | --image-name)
                check_arg 1 "$@"
                IMAGE_NAME=$2
                shift 2
                ;;
            -c | --container-name)
                check_arg 1 "$@"
                CONTAINER_NAME=$2
                shift 2
                ;;
            -b | --no-browser)
                check_arg 0 "$@"
                LAUNCH_BROWSER=0
                shift
                ;;
            -d | --detach)
                check_arg 0 "$@"
                DETACH=1
                shift
                ;;
            -h | --help)
                show_help
                exit 0
                ;;
            *)
                { show_usage && echo "Error: unrecognized argument: $1"; } >&2
                exit 1
                ;;
        esac
    done

    # readonly all values after updating defaults with args passed
    readonly IMAGE_NAME
    readonly CONTAINER_NAME
    readonly LAUNCH_BROWSER
    readonly DETACH
}


check_arg() {
    # helper function for option parsing
    # prints usage on exit if the caller is the main argument parser (parse_args)
    if (( "$1" )) && { [ -z "$3" ] || [ "${3:0:1}" == "-" ]; }; then
        # $1 == 1 if option requires value
        {
            echo "Error: option $2 requires one argument"
            [[ "${FUNCNAME[1]}" == "parse_args" ]] && show_usage;
        } >&2
        exit 1
    elif (( ! "$1" )) && [ -n "$3" ] && [ "${3:0:1}" != "-" ]; then
        # $1 == 0 if option is a boolean flag
        {
            echo "Error: unrecognized argument: $3"
            [[ "${FUNCNAME[1]}" == "parse_args" ]] && show_usage;
        } >&2
        exit 1
    fi
}


show_usage() {
    echo "launch_notebooks.sh [-h] [-d] [-b] [-i NAME] [-c NAME]"
}


show_help() {
    local long_description="Launch a Jupyter notebook server inside a Docker \
        container for running the analysis notebooks. The container is set up \
        automatically the first time the script is run."
    local -a options=(
        '-h, --help'
        '-d, --detach'
        '-b, --no-browser'
        '-i, --image-name NAME'
        '-c, --container-name NAME'
    )
    local -a descriptions=(
        'Show this help message and exit'
        'Don'\''t attach the terminal to the streaming notebook server log'
        'Don'\''t try to automatically open notebooks in a browser window'
        'Run a container from existing image NAME, or build a new image and tag it NAME'
        'Start the existing container NAME, or create a new container named NAME'
    )
    local -i option_indent=3
    local -i description_offset=4
    local -i max_cols=80
    local -i term_width
    term_width=$(get_terminal_width)
    (( term_width < max_cols )) && max_cols=$term_width
    local -i max_option_len="${#options[0]}"
    for opt in "${options[@]:1}"; do
        (( "${#opt}" > max_option_len )) && max_option_len="${#opt}"
    done

    local -i description_newline_indent=$(( option_indent + max_option_len + description_offset ))

    show_usage
    echo
    echo_block -c $max_cols "$long_description"
    printf '\nOptions:\n'
    for (( ix = 0; ix < "${#options[@]}"; ix++ )); do
        local opt="${options[ix]}"
        local -i curr_option_len="${#opt}"
        local -i curr_description_offset=$(( max_option_len - curr_option_len + description_offset ))
        printf '%*s%s%*s' $option_indent '' "$opt" $curr_description_offset ''
        echo_block -i $description_newline_indent -c $max_cols "${descriptions[ix]}"
    done
}


########################################
#           HELPER FUNCTIONS           #
########################################
is_executable() {
    [ -x "$(command -v "$1")" ]
}


get_terminal_width() {
    # tries to use terminfo, then falls back to COLUMNS env var, then falls back to standard cpl
    tput cols 2> /dev/null || echo "${COLUMNS:-80}"
}


echo_block() {
    local str
    local -i indent=0
    local -i max_cols="${COLUMNS:-80}"
    local -a word_arr
    while (( "$#" )); do
        case "$1" in
            -i | --indent)
                check_arg 1 "$@"
                indent=$2
                shift 2
                ;;
            -c | --max-cols)
                check_arg 1 "$@"
                max_cols=$2
                shift 2
                ;;
            -*)
                echo "Error: unrecognized argument: $1" >&2
                exit 1
                ;;
            *)
                if [ -n "$str" ]; then
                    echo "Error: content to be echoed must be passed as a single argument" >&2
                    exit 1
                else
                    str=$1
                    shift
                fi
                ;;
        esac
    done

    IFS=' ' read -ra word_arr <<< "$str"
    local -i char_ix=$indent
    for word in "${word_arr[@]}"; do
        local -i word_len="${#word}"
        (( char_ix += word_len + 1 ))
        if (( char_ix > max_cols )); then
            printf '\n%*s' $indent ''
            (( char_ix = indent + word_len + 1 ))
        fi

        printf '%s ' "$word"
    done
    printf '\n'
}


fancy_echo() {
    local str
    local pad_chars="="
    local -i full_width
    local lpad
    local rpad

    while (( "$#" )); do
        case "$1" in
            -p | --pad-character)
                check_arg 1 "$@"
                pad_chars=$2
                shift 2
                ;;
            -w | --width)
                check_arg 1 "$@"
                full_width=$2
                shift 2
                ;;
            -*)
                echo "Error: unrecognized argument: $1" >&2
                exit 1
                ;;
            *)
                if [ -n "$str" ]; then
                    echo "Error: content to be echoed must be passed as a single argument" >&2
                    exit 1
                else
                    str=$1
                    shift
                fi
                ;;
        esac
    done

    [ -n "$str" ] && str=" $str " || str=""
    [ -z "$full_width" ] && full_width=$(get_terminal_width)

    local -i str_width="${#str}"
    local -i lpad_len=(full_width-str_width)/2
    local -i rpad_len=full_width-str_width-lpad_len

    if (( lpad_len > 0)) && (( rpad_len > 0)); then
        printf -v lpad "$pad_chars%.0s" $(seq "$lpad_len")
        printf -v rpad "$pad_chars%.0s" $(seq "$rpad_len")
    fi

    printf "%s%s%s\n" "$lpad" "$str" "$rpad"
}


########################################
#           DOCKER FUNCTIONS           #
########################################
catch_daemon_failures() {
    # trap function for dealing with errors related to Docker daemon
    if [[ "$1" == "127" ]]; then
        # triggered by daemon_is_running if Docker isn't installed
        echo "Docker does not appear to be installed on your system. See the README for installation instructions." >&2
        exit 1
    elif [[ "$1" == "253" ]]; then
        # triggered by attempt_start_daemon if none of the 3 common utilities
        # that can start Docker are available
        echo "Couldn't determine how to start the Docker daemon automatically. Please start the daemon manually and try again." >&2
        exit 1
    elif [[ "$1" == "254" ]]; then
        # triggered by attempt_start_daemon if the daemon still isn't running
        # 30s after starting it
        if (( is_mac )); then
            osascript -e "quit app \"Docker\""
        elif ps -p "$daemon_start_pid" > /dev/null 2>&1; then
            kill "$daemon_start_pid"
        fi
        echo "Docker daemon failed to start after 30 seconds. Please start the daemon manually and try again." >&2
        exit 1
    elif [[ "$1" != "0" ]]; then
        # catch-all for reporting unexpected exit codes
        echo "Error $1 occurred in line $2" >&2
        exit 1
    fi
}


daemon_is_running() {
    # handles checks for both whether the Docker daemon is running and whether
    # Docker is installed:
    #   - if running, returns 0
    #   - if installed but not running, returns 1
    #   - if not installed, triggers catch_daemon_failures trap with exit 127
    #   - if command exits with any other code, triggers generic error message in trap
    docker info > /dev/null 2>&1
    local -i status=$?
    [[ "$status" -gt "1" ]] && exit $status || return $status
}


attempt_start_daemon() {
    # https://docs.docker.com/config/daemon/systemd/
    if (( is_mac )); then
        open -ga Docker &
    elif is_executable systemctl; then
        systemctl start docker &
    elif is_executable service; then
        service docker start &
    else
        exit 253
    fi

    daemon_start_pid=$!
    local -i n_attempts
    printf "starting Docker daemon (this may take a minute) "
    while ! daemon_is_running; do
        if [ $(( n_attempts++ )) -ge 30 ]; then
            exit 254
        else
            printf "."
            sleep 1
        fi
    done
    # adds a newline after dynamic printf'd output
    echo
}


check_docker_daemon() {
    if ! daemon_is_running; then
        attempt_start_daemon
    fi
}


local_image_exists() {
    [ -n "$(docker image ls -qf "reference=$IMAGE_NAME")" ]
}


build_local_image() {
    fancy_echo "building image: $IMAGE_NAME"
    docker build \
        --rm \
        --force-rm \
        --build-arg WORKDIR="/mnt/$NOTEBOOKS_DIR" \
        --build-arg NB_PORT="$CONTAINER_PORT" \
        -t "$IMAGE_NAME" \
        -f "$repo_root/$DOCKERFILE_PATH" \
        "$repo_root"
}


container_exists() {
    [ -n "$(docker ps -aqf "name=^$CONTAINER_NAME$")" ]
}


create_container() {
    echo "creating new container: $CONTAINER_NAME"
    docker create \
        -it \
        -p "$LOCAL_PORT":"$CONTAINER_PORT" \
        -v "$repo_root:/mnt" \
        --name "$CONTAINER_NAME" \
        "$IMAGE_NAME" \
        > /dev/null
}


start_container() {
    ! local_image_exists && build_local_image
    ! container_exists && create_container
    # record container start time to show relevant notebook server logs in case of failure
    echo "starting container"
    container_start_time=$(date +%s)
    docker start "$CONTAINER_NAME" > /dev/null
    docker exec "$CONTAINER_NAME" bash -c "jupyter notebook"
}


########################################
#          NOTEBOOK FUNCTIONS          #
########################################
get_nbserver_url() {
    local running_nbserver
    running_nbserver=$(docker exec "$CONTAINER_NAME" bash -c 'jupyter notebook list')
    local url_dir_info="${running_nbserver#Currently running servers:}"
    nbserver_url="${url_dir_info%% *}"
    nbserver_url="${nbserver_url//$'\n'}"
}


wait_for_nbserver() {
    fancy_echo "launching notebook server"
    local -i attempts
    local shutdown_instruction
    while [ -z "$nbserver_url" ]; do
        if [ $(( attempts++ )) -ge 10 ]; then
            {
                echo "notebook server failed to launch"
                fancy_echo "server logs:"
                docker logs "$CONTAINER_NAME" --since "$container_start_time"
                fancy_echo
            } >&2
            exit 1
        fi

        get_nbserver_url
    done

    if (( DETACH )); then
        shutdown_instruction="Enter 'docker stop $CONTAINER_NAME'"
    else
        shutdown_instruction="Press Control-c"
    fi

    echo "server running at:"
    printf "\t%s\n\n" "$nbserver_url"
    echo "$shutdown_instruction to exit and stop the notebook server and container"
}


attempt_launch_browser() {
    if (( is_mac )); then
        # Mac command counterpart
        open "$nbserver_url"
    elif [ -n "$BROWSER" ]; then
        # prefer BROWSER environment variable, if set
        "$BROWSER" "$nbserver_url"
    elif is_executable xdg-open; then
        # use xdg-utils if installed (most common for linux)
        xdg-open "$nbserver_url"
    elif is_executable gnome-open; then
        # also try gnome if no others work
        gnome-open "$nbserver_url"
    fi
}


########################################
#                 MAIN                 #
########################################
main() {
    local repo_root
    local -i is_mac
    local -i container_start_time
    local nbserver_url

    parse_args "$@"

    repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
    [[ $(uname) == "Darwin" ]] && is_mac=1 || is_mac=0
    readonly repo_root
    readonly is_mac

    trap 'catch_daemon_failures $? $LINENO' EXIT
    check_docker_daemon
    trap '' EXIT

    start_container
    wait_for_nbserver
    (( LAUNCH_BROWSER )) && attempt_launch_browser
    ! (( DETACH )) && docker attach "$CONTAINER_NAME"
}


main "$@"

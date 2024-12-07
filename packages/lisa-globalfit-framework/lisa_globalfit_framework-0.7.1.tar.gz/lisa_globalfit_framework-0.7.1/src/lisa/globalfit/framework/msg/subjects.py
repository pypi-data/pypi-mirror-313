from collections.abc import Callable

Subject = str

SUBJECT_SCIENCE = Subject("sci")
SUBJECT_INFRA = Subject("infra")

SUBJECT_GLOBALFIT = Subject(f"{SUBJECT_SCIENCE}.gf")

PERSISTENT_SUBJECTS = [SUBJECT_SCIENCE, SUBJECT_INFRA]

ANY_SUBJECT = "*"


def create_channel_name(*args: str) -> Subject:
    return ".".join(
        [
            SUBJECT_SCIENCE,
            "gf",
            *args,
        ]
    )


def channel_any(channel_fn: Callable) -> Subject:
    return channel_fn(
        ".".join([SUBJECT_GLOBALFIT, ANY_SUBJECT, ANY_SUBJECT, ANY_SUBJECT])
    )


def channel_any_group_any_module(run_id: Subject, channel_fn: Callable) -> Subject:
    return channel_fn(".".join([SUBJECT_GLOBALFIT, run_id, ANY_SUBJECT, ANY_SUBJECT]))


def channel_get_pipeline(channel: Subject) -> str:
    return channel.split(".")[2]


def channel_get_group(channel: Subject) -> str:
    return channel.split(".")[3]


def channel_get_module(channel: Subject) -> str:
    return channel.split(".")[4]


def channel_strip(sub: Subject) -> Subject:
    return ".".join(sub.split(".")[:-2])


def channel_configure(sub: Subject) -> Subject:
    return f"{sub}.control.configure"


def channel_iterate(sub: Subject) -> Subject:
    return f"{sub}.control.iterate"


def channel_terminate(sub: Subject) -> Subject:
    return f"{sub}.control.terminate"


def channel_status(sub: Subject) -> Subject:
    return f"{sub}.control.status"


def channel_data_state(sub: Subject) -> Subject:
    return f"{sub}.data.state"

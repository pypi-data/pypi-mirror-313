# These two fields will show up within `metaflow_version` task metadata.
# Setting to major version of ob-metaflow-extensions only, so we don't keep trying
# (and failing) to keep this in sync with setup.py
# E.g. "2.7.22.1+ob(v1)"
__version__ = "v1"
__mf_extensions__ = "ob"


# Must match the signature of metaflow.plugins.aws.aws_client.get_aws_client
# This function is called by the "userland" code inside tasks. Metaflow internals
# will call the function in metaflow.plugins.aws.aws_client.get_aws_client directly.
#
# Unlike the original function, this wrapper will use the CSPR role if both of the following
# conditions are met:
#
#  1. CSPR is set
#  2. user didn't provide a role to assume explicitly.
#
def get_aws_client(
    module, with_error=False, role_arn=None, session_vars=None, client_params=None
):
    import metaflow.plugins.aws.aws_client

    from metaflow_extensions.outerbounds.plugins import USE_CSPR_ROLE_ARN_IF_SET

    return metaflow.plugins.aws.aws_client.get_aws_client(
        module,
        with_error=with_error,
        role_arn=role_arn or USE_CSPR_ROLE_ARN_IF_SET,
        session_vars=session_vars,
        client_params=client_params,
    )


# This should match the signature of metaflow.plugins.datatools.s3.S3.
#
# This assumes that "userland" code inside tasks will call this, while Metaflow
# internals will call metaflow.plugins.datatools.s3.S3 directly.
#
# This wrapper will make S3() use the CSPR role if its set, and user didn't provide
# a role to assume explicitly.
def S3(*args, **kwargs):
    import sys
    import metaflow.plugins.datatools.s3
    from metaflow_extensions.outerbounds.plugins import USE_CSPR_ROLE_ARN_IF_SET

    if "role" not in kwargs or kwargs["role"] is None:
        kwargs["role"] = USE_CSPR_ROLE_ARN_IF_SET

    return metaflow.plugins.datatools.s3.S3(*args, **kwargs)


from .. import profilers

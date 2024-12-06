from osbot_utils.helpers.trace.Trace_Call import trace_calls

# here are all the trace_calls options:
#
#     title         = None , print_traces = True , show_locals    = False, source_code          = False ,
#     ignore        = None , include      = None , show_path      = False, duration_bigger_than = 0     ,
#     trace_depth   = 0    , max_string   = None , show_types     = False, show_duration        = False ,
#     show_class    = False, contains     = None , show_internals = False, enabled              = True  ,
#     extra_data    = False, show_lines   = False, print_lines    = False, show_types_padding   = None  , duration_padding=None):

# good ignore list

# ignore=['TestClient', 'httpx', 'urllib', 'inspect', 'starlette', 'asyncio', 're',
#         'namedtuple_ParseResult', 'http', 'contextlib', 'anyio',
#         'functools', 'collections', 'threading', 'concurrent', 'typing',
#         '_weakrefset', 'enum', 'namedtuple_DoneAndNotDoneFutures',
#         'email', 'namedtuple_SplitResult', 'logging']

DEFAULT_TRACE__KWARGS__CBR = dict(include          = ["cbr"],
                                  show_class       =  True               ,
                                  show_duration    = True                ,
                                  duration_padding = 120                 )

def cbr_trace_calls(*args, **outer_kwargs):
    def decorator(func):
        # Combine the fixed arguments with the additional keyword arguments
        trace_calls_args = DEFAULT_TRACE__KWARGS__CBR
        trace_calls_args.update(outer_kwargs)
        return trace_calls(**trace_calls_args)(func)

    if len(args) == 1 and callable(args[0]):
        # The decorator is used without arguments
        return decorator(args[0])
    else:
        # The decorator is used with arguments
        return decorator
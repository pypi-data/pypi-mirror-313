#**************************************************************************
# * Copyright (C) 2023-present Bert Van Acker (B.MKR) <bva.bmkr@gmail.com>
# *
# * This file is part of the hybridIO project.
# *
# * HybridIO can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# *************************************************************************

class OrchestrationType:
    FMI_local = "FMI_LOCAL"
    DISTRIBUTED = "DISTRIBUTED"
    DISTRIBUTED_FIXED_IO = "DISTRIBUTED_FIXED_IO"

class ExecutionPatterns:
    TRIGGERED = "TRIGGERED"
    IPO = "IPO"
    IOP = "IOP"

class VerificationMethods:
    STATICLOWERBOUND = "StaticLowerBound"
    STATICUPPERBOUND = "StaticUpperBound"
    STATICBOUND = "StaticBound"

class MonitorType:
    RUNTIME = "runtime"
    POSTPROCESSING = "postprocessing"
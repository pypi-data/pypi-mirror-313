from enum import Enum


class LAYER(str,Enum):
    I_D_R = "infrastructure/database/repositories"
    D_S_U_E = "domain/services/use_cases/entities"
    I_W_C_E = "infrastructure/web/controller/entities"
    D_S_U_A_P_E = "domain/services/use_cases/apis/platform/entities"
    I_A_P_R_E = "infrastructure/apis/platform/repositories/entities"

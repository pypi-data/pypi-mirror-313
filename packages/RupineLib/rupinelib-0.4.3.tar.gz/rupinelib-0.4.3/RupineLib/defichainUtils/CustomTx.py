from dataclasses import dataclass

@dataclass
class CustomTxType:
    Reject:str = 1
    # masternodes:
    CreateMasternode:str = 'C'
    ResignMasternode:str = 'R'
    UpdateMasternode:str = 'm'
    SetForcedRewardAddress:str = 'F'
    RemForcedRewardAddress:str = 'f'
    
    # custom tokens:
    CreateToken:str = 'T'
    MintToken:str   = 'M'
    UpdateToken:str = 'N' # previous type, only DAT flag triggers
    UpdateTokenAny:str = 'n' # new type of token's update with any flags/fields possible
    
    # dex orders - just not to overlap in future
    # CreateOrder:str = 'O'
    # DestroyOrder:str = 'E'
    # MatchOrders:str = 'A'
    
    # poolpair
    CreatePoolPair:str = 'p'
    UpdatePoolPair:str = 'u'
    PoolSwap:str = 's'
    PoolSwapV2:str = 'i'
    AddPoolLiquidity:str = 'l'
    RemovePoolLiquidity:str = 'r'
    
    # accounts
    UtxosToAccount:str = 'U'
    AccountToUtxos:str = 'b'
    AccountToAccount:str = 'B'
    AnyAccountsToAccounts:str = 'a'
    SmartContract:str = 'K'
    DFIP2203:str = 'Q'
    # set governance variable
    SetGovVariable:str = 'G'
    SetGovVariableHeight:str = 'j'
    # Auto auth TX
    AutoAuthPrep:str  = 'A'
    # oracles
    AppointOracle:str = 'o'
    RemoveOracleAppoint:str = 'h'
    UpdateOracleAppoint:str = 't'
    SetOracleData:str = 'y'
    # ICX
    ICXCreateOrder:str = '1'
    ICXMakeOffer:str = '2'
    ICXSubmitDFCHTLC:str = '3'
    ICXSubmitEXTHTLC:str = '4'
    ICXClaimDFCHTLC:str = '5'
    ICXCloseOrder:str = '6'
    ICXCloseOffer:str = '7'
    
    # Loans
    SetLoanCollateralToken:str = 'c'
    SetLoanToken:str = 'g'
    UpdateLoanToken:str = 'x'
    LoanScheme:str = 'L'
    DefaultLoanScheme:str = 'd'
    DestroyLoanScheme:str = 'D'
    Vault:str = 'V'
    CloseVault:str = 'e'
    UpdateVault:str = 'v'
    DepositToVault:str = 'S'
    WithdrawFromVault:str = 'J'
    TakeLoan:str = 'X'
    PaybackLoan:str = 'H'
    PaybackLoanV2:str = 'k'
    AuctionBid:str = 'I'
    
    # Marker TXs
    FutureSwapExecution:str = 'q'
    FutureSwapRefund:str = 'w'

@dataclass
class OPCodes:
    OP_RETURN:str = '6a'
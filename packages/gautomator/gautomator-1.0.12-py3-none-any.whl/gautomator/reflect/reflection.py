from functools import partial
from gautomator.protocol.common import OPStaticFunction, OPNonStaticFunction

static_method = partial(OPStaticFunction, True)
non_static_method = partial(OPNonStaticFunction, False)

ga_private = partial(static_method, "/Script/GAExtension", "GAReflectionExtension")
GameplayStatics = partial(static_method, '/Script/Engine', 'GameplayStatics')
WidgetBlueprintLibrary = partial(static_method, '/Script/UMG', 'WidgetBlueprintLibrary')
KismetSystemLibrary = partial(static_method, '/Script/Engine', 'KismetSystemLibrary')
AbilitySystemBlueprintLibrary = partial(
    static_method, '/Script/GameplayAbilities', 'AbilitySystemBlueprintLibrary')
GPASC = partial(static_method, '/Script/GPAbility', 'GPASC')
GameFrameWork = partial(static_method, '/Script/GameFrameWork', 'NZHelper')
AnalysisServiceBPLib = partial(static_method, '/Script/AnalysisService', 'AnalysisServiceBPLib')
CitySampleBlueprintLibrary = partial(static_method, '/Script/CitySample', 'CitySampleBlueprintLibrary')
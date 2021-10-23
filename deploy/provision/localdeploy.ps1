$ArmTemplate = ".\arm.json"
$ParameterFile = ".\armParameters.json"
$ResourceGroup = "AISHUEH-Health-Hub-Sandbox"
$Subscription = "98344f52-981f-4656-9ee4-3910e834889b"

az deployment group create `
    --template-file $ArmTemplate `
    --parameters $ParameterFile `
    -g $ResourceGroup `
    --subscription $Subscription
module Producer

open System
open System.IO
open Microsoft.AspNetCore.Mvc
open Microsoft.Azure.WebJobs
open Microsoft.Azure.WebJobs.Extensions.Http
open Microsoft.AspNetCore.Http
open Newtonsoft.Json
open Microsoft.Extensions.Logging

open Samples
open Service

[<FunctionName("GetUserSamples")>]
let run (
    [<HttpTrigger(AuthorizationLevel.Function, "get", Route = "usersample" )>]req: HttpRequest) 
    (log: ILogger) =
        async {
            let allSSn = Samples.getSsns()
            let maleNames = Samples.getMaleNames()
            let femaleNames = Samples.getFemaleNames()
            let lastNames = Samples.getLastNames()

            let maleSsn = allSSn |> getMaleSsns
            let femaleSsn = allSSn |> getFemaleSsns

            let rnd = System.Random()
            
            let _createUser = 
                createGenderSpecificUser 
                    rnd lastNames maleSsn maleNames femaleSsn femaleNames

            let r = 
                10
                |> pickMaleAndFemales rnd
                |> List.toArray
                |> Array.map (_createUser)

            return OkObjectResult(r) :> IActionResult
        } |> Async.StartAsTask
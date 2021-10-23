$slnName = "Azure"
$buildDir = "$PSScriptRoot/build"

$artifactDir = "$buildDir/artifacts"
$artifactZipName = "$slnName.zip"

$dotnetDir = "$buildDir/dotnet" 
$rootDir = "$PSScriptRoot/../"
$slnPath = "$rootDir/$slnName.sln"

$provisionDir = "$PSScriptRoot/provision"

function clean([string]$p){
    if (Test-Path $p) { Remove-Item $p -Recurse}
    New-Item -Path $p -ItemType directory
}

function build([string] $slnPath, [string] $dotnetDir) {
    dotnet build --output $dotnetDir --configuration "Release" $slnPath
}

function createFolder([string] $path) {
    New-Item -Path $path -ItemType directory
}

function copyToDir([string] $sourceDir, [string] $destinationDir) {
    Copy-Item -Path $sourceDir -Destination $destinationDir -Recurse
}

function zip([string] $source, [string] $destination) {
    Compress-Archive -Path $source -DestinationPath $destination
}

clean $buildDir
build $slnPath $dotnetDir

createFolder $artifactDir
zip "$dotnetDir/*" "$artifactDir/$artifactZipName"

copyToDir "$provisionDir/*" $artifactDir
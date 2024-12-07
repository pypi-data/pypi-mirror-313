#!/bin/bash

fname="${1%%.cs}"

if [ "${fname}.cs" != "$1" ]; then
    echo "Wrong C# filename: ${1}"
    exit 1
fi

dotnetVersion=$(dotnet --version)

if [[ "$dotnetVersion" =~ ^([0-9]+[.][0-9]+)[.][0-9]+$ ]]; then
    dotnetversion=${BASH_REMATCH[1]}
else
    echo "No dotnet system detected"
    exit 1
fi

pname="${fname}-prj"
mkdir -p "_build/${pname}"

cat > "_build/${pname}/${pname}.csproj" << --END--
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>netcoreapp${dotnetversion}</TargetFramework>
    <TieredCompilation>false</TieredCompilation>
    <Optimize>true</Optimize>
  </PropertyGroup>
  <ItemGroup>
    <Compile Include="../../$1" Link="$1" />
  </ItemGroup>
</Project>
--END--

cd "_build/$pname"
dotnet publish -c Release -v q #-p:PublishReadyToRun=true -r linux-x64
retVal=$?
if [ $retVal -ne 0 ]; then
	exit $retVal
fi
cd "../.."
ln -sf "${pname}/bin/Release/netcoreapp${dotnetversion}/publish/${pname}" "_build/${fname}-cs.exe" 

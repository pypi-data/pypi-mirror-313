# Snapser CLI

Snapser has developed a CLI tool called **snapctl** that can be used on MaxOSX, Linux and Windows machines.
Snapctl will be the best way for game studios to integrate Snapser into their build pipelines.

### Python 3.X and Pip
The Snapser CLI tool depends on Python 3.X and Pip. MacOS comes pre installed with Python. But
please make sure you are running Python 3.X. On Windows, you can download Python 3.X from the
Windows store.

### Docker
Some of the commands also need docker. You can download the latest version of Docker from the
[Docker website](https://www.docker.com/products/docker-desktop).

**IMPORTANT**: Open up Docker desktop and settings. Make sure this setting is disabled
**Use containerd for pulling and storing images**. This is because Snapser uses Docker
to build and push images to the Snapser registry. Having this setting enabled will
cause issues with the Snapser CLI tool.

## Installation

Installing PIP on MacOS

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

Installing PIP on Windows

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

Once you have Python and Pip installed

```
pip install --user snapctl
```

If you also have Python 2.X on your machine, you may have to run the following command instead

```
pip3 install --user snapctl
```

**IMPORTANT**: After you install snapctl you may have to add the python bin folder to your
path. For example, on MacOSX this is usually **~/Library/Python/3.9/bin**. On
Windows this is usually
**C:\Users\username\AppData\Roaming\Python\Python39\Scripts**.

## Upgrade

Upgrade your snapctl version

```
pip install --user snapctl --upgrade
```

## Setup

### Get your Snapser Access Key

Log in to your Snapser account. Click on your user icon on the top right and select, User Account.
In the left navigation click on **Developer** which will bring up your Personal API Key widget.
If you have not generated an API Key yet click on the **Generate** button to generate a new key.
You can generate up to 3 API Keys per user account.

**IMPORTANT**: Please make sure you save your API key in a safe place. You will not be able
to see it again.

### Setup a local config

You have three ways to pass the API key to Snapctl
1. Pass it via a command line argument with every command
2. Pass it via an environment variable
3. Pass it via a config file

#### Command line argument

Every Snapser command can take a command line argument `--api-key <your_key>`. This will take precedence over
other methods.

#### Environment Variable

You can set an Environment variable `SNAPSER_API_KEY=<your_key>` and then run your snapctl commands. This will
be evaluated after verifying if there is any command line argument.

#### Config file

Create a file named `~/.snapser/config`. Open it using the editor of your choice and replace with your
personal Snapser Access key. Save the file. Advantage of using this method is you can use the `--profile`
argument with your snapctl command to use different API keys. NOTE: You may want to pass your own path
instead on relying on the default one the CLI looks for. You can do so by setting an environment
variable `SNAPSER_CONFIG_PATH='<your_custom_path>'`. Doing this will make sure that the CLI tool
will look for the config file at that path.

```
[default]
snapser_access_key = <key>
```

Or you can run the following command

on MacOSX

```
# $your_api_key = Your Snapser developer key
echo -e "[default]\nSNAPSER_API_KEY=$your_api_key" > ~/.snapser/config
```

on Windows Powershell

```
# $your_api_key = Your Snapser developer key
echo "[default]
SNAPSER_API_KEY=$your_api_key" | Out-File -encoding utf8 ~\.snapser\config
```

## Verify Snapctl installation

```
snapctl validate
```

Output will tell you if the Snapctl was able successfully validate your setup with the remote Snapser server
or not.

## Advanced Setup

Snapser by default supports access to multiple accounts. You can create multiple profiles in your Snapser config
**~/.snapser/config**.

```
[profile personal]
snapser_access_key = <key>

[profile professional]
snapser_access_key = <key>

```

You can then set an environment variable telling Snapser which profile you want to use.

```
# Mac
export SNAPSER_PROFILE="my_profile_name";

```

```
# Windows
setx SNAPSER_PROFILE="my_profile_name";

```

Or you can pass **--profile my_profile_name** with every command to tell Snapser to use a particular profile.

## Commands

Run the following to see the list of commands Snapser supports

```
snapctl --help
```

### BYO Snap - Bring your own Snap
Snapctl commands for your custom code

#### 1. byosnap help

See all the supported commands

```
# Help for the byosnap command
snapctl byosnap --help
```

#### 2. byosnap create

Create a custom snap. Note that you will have to build, push and publish your snap image, for it to be useable
in a Snapend.

```
# Help for the byosnap command
snapctl byosnap create --help

# Create a new snap
# $byosnap_sid = Snap ID for your snap. Start start with `byosnap-`
# $name = User friendly name for your BYOSnap
# $desc = User friendly description
# $platform = One of linux/arm64, linux/amd64
# $language = One of go, python, ruby, c#, c++, rust, java, node

# Example:
# snapctl byosnap create byosnap-jinks-flask --name "Jinks Flask Microservice" --desc "Custom Microservice" --platform "linux/arm64" --language "go"
snapctl byosnap create $byosnap_sid --name "$name" --desc "$desc" --platform "$platform" --language "$language"
```

#### 3. byosnap build

Build your snap image

```
# Help for the byosnap command
snapctl byosnap build --help

# Publish a new image
# $byosnap_sid = Snap ID for your snap
# $image_tag = An image tag for your snap
# $code_root_path = Local code path where your Dockerfile is present
# $resources_path = Optional path to the resources directory in your Snap. This ensures, you are not forced to put the Dockerfile, swagger.json and README.md in the root directory of your Snap.
# Example:
# snapctl byosnap build byosnap-jinks-flask --tag my-first-image --path /Users/DevName/Development/SnapserEngine/jinks_flask
snapctl byosnap build $byosnap_sid --tag $image_tag --path $code_root_path
snapctl byosnap build $byosnap_sid --tag $image_tag --path $code_root_path --resources-path $resources_path
```

#### 4. byosnap push

Push your snap image to Snapser

```
# Help for the byosnap command
snapctl byosnap push --help

# Publish a new image
# $byosnap_sid = Snap ID for your snap
# $image_tag = An image tag for your snap
# Example:
# snapctl byosnap push byosnap-jinks-flask --tag my-first-image
snapctl byosnap push $byosnap_sid --tag $image_tag
```

#### 5. byosnap upload-docs

Upload swagger.json and README.md for you Snap

```
# Help for the byosnap command
snapctl byosnap upload-docs --help

# Publish a new image
# $byosnap_sid = Snap ID for your snap
# $image_tag = An image tag for your snap
# $resources_path = Path to your swagger.json and README.md files
# Example:
# snapctl byosnap upload-docs byosnap-jinks-flask --tag my-first-image --resources-path /Users/DevName/Development/SnapserEngine/jinks_flask
snapctl byosnap upload-docs $byosnap_sid --tag $image_tag --resources-path $resources_path
```

#### 6. byosnap publish-image

Publish a custom snap code image. This command executes, `build`, `push` and `upload-docs` one
after the other.

**IMPORTANT**: Take note of the hardware architecture of machine and your Dockerfile commands.
Commands in docker file may be hardware architecture specific. Snapser throws a warning if it detects
a mismatch.

```
# Help for the byosnap command
snapctl byosnap publish-image --help

# Publish a new image
# $byosnap_sid = Snap ID for your snap
# $image_tag = An image tag for your snap
# $code_root_path = Local code path where your Dockerfile is present
# $resources_path = Optional path to the resources directory in your Snap. This ensures, you are not forced to put the Dockerfile, swagger.json and README.md in the root directory of your Snap.
# $skip-build = true/false. Default is false. Pass this flag as true to skip the build and head straight to tag and push. Build step needs to run and tagged using the --tag you pass to the publish-image command for this to work.
# Example:
# snapctl byosnap publish-image byosnap-jinks-flask --tag my-first-image --path /Users/DevName/Development/SnapserEngine/jinks_flask
snapctl byosnap publish-image $byosnap_sid --tag $image_tag --path $code_root_path
snapctl byosnap publish-image $byosnap_sid --tag $image_tag --path $code_root_path --resources-path $resources_path
snapctl byosnap publish-image $byosnap_sid --tag $image_tag --skip-build
```

#### 7. byosnap publish-version

Publish a new version for your Snap. Only after your Snap version is published, you will be able
to use your snap in your Snapend. This command should be run after `push` or `publish-image` commands.

IMPORTANT: You need to have $byosnapProfile to run this command. BYOSnap profile is a JSON configuration
of your BYOSnap for the development, staging and production environments. You can generate a base version of this file using the `snapctl generate profile --category byosnap --out-path <output_path>` command.

```
# Help for the byosnap command
snapctl byosnap publish-version --help

# Publish a new image
# $byosnap_sid = Snap ID for your snap
# $image_tag = An image tag for your snap
# $prefix = Prefix for your snap Eg: /v1
# $version = Semantic version for your snap Eg: v0.0.1
# $ingress_port = Ingress port for your snap Eg: 5003
# $byosnap_profile = BYOSnap profile to configure dev, stage and prod settings for this snap. You can generate a base version of this file using the `snapctl generate profile --category byosnap --out-path <output_path>` command
# Example:
# snapctl byosnap publish-image byosnap-jinks-flask --tag my-first-image --prefix /v1 --version v0.0.1 --http-port 5003 --byosnap-profile /Users/DevName/Development/SnapserEngine/jinks_flask/snapser-byosnap-profile.json
snapctl byosnap publish-version $byosnap_sid --tag $image_tag --prefix $prefix --version $version --http-port $ingress_port --byosnap-profile $byosnap_profile
```

#### 8. byosnap sync

This command is for development purposes. It allows developers to rapidly build, update and push their
BYOSnap to a dev Snapend. Simply, make changes to your code locally, and then run this command to deploy
your BYOSnap straight to your development Snapend.

IMPORTANT: This command will only work for Dev Snapends. Additionally if the tag you are using in this
command happens to be used by a staging or a production snapend then `sync` will not work. We do this to
ensure that your staging and production BYOSnap images do not get impacted.

```
# Help for the byosnap command
snapctl byosnap sync --help

# Publish a new image
# $byosnap_sid = Snap ID for your snap
# $code_root_path = Local code path where your Dockerfile is present
# $resources_path = Optional path to the resources directory in your Snap. This ensures, you are not forced to put the Dockerfile, swagger.json and README.md in the root directory of your Snap.
# $skip-build = true/false. Default is false. Pass this flag as true to skip the build and head straight to tag and push. Build step needs to run and tagged using the --tag you pass to the publish-image command for this to work.
# $image_tag = An image tag for your snap. Note snapctl adds a timestamp, allowing you to use the same command.
# $version = Semantic version for your snap Eg: v0.0.1
# $snapend_id = Dev Snapend Id
# Example:
snapctl byosnap sync byosnap-jinks-flask --path /Users/DevName/Development/SnapserEngine/jinks_flask --tag my-first-image --version "v0.0.11" --snapend-id "jxmmfryo"
snapctl byosnap sync $byosnap_sid --path $code_root_path --tag $image_tag --version $version --snapend-id $snapend_id
```

### BYO Game Server - Bring your own Game Server
Snapctl commands for your custom game server

#### 1. byogs help

See all the supported commands

```
# Help for the byogs command
snapctl byogs --help
```

#### 2. byogs build

Build your custom game server image.

```
# Help for the byogs command
snapctl byogs build --help

# Publish a new image
# $image_tag = An image tag for your snap
# $code_root_path = Local code path where your Dockerfile is present
# Example:
# snapctl byogs build byosnap-jinks-gs --tag my-first-image --path /Users/DevName/Development/SnapserEngine/game_server
snapctl byogs build --tag $image_tag --path $code_root_path
```

#### 3. byogs push

Push your custom game server image.

```
# Help for the byogs command
snapctl byogs push --help

# Publish a new image
# $image_tag = An image tag for your snap
# Example:
# snapctl byogs push byosnap-jinks-gs --tag my-first-image
snapctl byogs push --tag $image_tag
```

#### 4. byogs publish

Publish your custom game server image. This commend replaces the old way of creating, publishing image and
then publishing the byogs. Now all you have to do is publish your image and create a fleet using the web portal.

**IMPORTANT**: Take note of the hardware architecture of machine and your Dockerfile commands.
Commands in docker file may be hardware architecture specific. Snapser throws a warning if it detects
a mismatch.

```
# Help for the byogs command
snapctl byogs publish --help

# Publish a new image
# $image_tag = An image tag for your snap
# $code_root_path = Local code path where your Dockerfile is present
# $resources_path = Optional path to the resources directory. This ensures, you are not forced to put the Dockerfile at the root directory of your Game Server code.
# $skip-build = Default is false. Pass this flag as true to skip the build and head straight to tag and push. Build step needs to run and tagged using the --tag you pass to the publish-image command for this to work.
# Example:
# snapctl byogs publish --tag my-first-image --path /Users/DevName/Development/SnapserEngine/game_server
snapctl byogs publish --tag $image_tag --path $code_root_path
snapctl byogs publish --tag $image_tag --path $code_root_path --resources-path $resources_path
snapctl byogs publish --tag $image_tag --skip-build
```

#### 5. byogs sync

This command allows developers to rapidly build, update and push their BYOGs out to a Snapend fleet. Simply, make changes to your code locally, and then run this command to deploy your BYOGs straight to your Snapend fleet.

```
# Help for the byogs command
snapctl byogs sync --help

# Publish a new image
# $code_root_path = Local code path where your Dockerfile is present
# $resources_path = Optional path to the resources directory in your Snap. This ensures, you are not forced to put the Dockerfile, swagger.json and README.md in the root directory of your Snap.
# $skip-build = true/false. Default is false. Pass this flag as true to skip the build and head straight to tag and push. Build step needs to run and tagged using the --tag you pass to the publish-image command for this to work.
# $image_tag = An image tag for your snap. Note snapctl adds a timestamp, allowing you to use the same command.
# $snapend_id = Snapend Id
# $fleet_names = Comma separated fleet names
# Example:
snapctl byogs sync --path /Users/DevName/Development/SnapserEngine/game_server --tag my-first-image --snapend-id "jxmmfryo" --fleet-names "my-fleet,my-second-fleet"
snapctl byosnap sync --path $code_root_path --tag $image_tag --snapend-id $snapend_id --fleet-names $fleet_names
```

### Game
Snapctl commands for your game

#### 1. game help

See all the supported commands

```
# Help for the byogs command
snapctl game --help
```

#### 2. Create a game
Create a game
```
snapctl game create --name $gameName
```

#### 3. Enumerate games
List all the games
```
snapctl game enumerate
```

### Generate
Generator tool to help generate base files to be used in other commands

#### 1. generate help
See all the supported commands
```
# Help for the generate command
snapctl generate --help
```

#### 2. Generate BYOSnap Profile
Generate the base file for BYOSnap profile to be used in the `snapctl byosnap publish-version` command

```
snapctl generate profile --category "byosnap" --out-path $output_path

```

#### 3. Generate ECR Credentials
Generate the ECR credentials. Game studios can use these credentials to self publish their images to Snapser.

```
snapctl generate credentials --category "ecr" --out-path $output_path

```

### Snapend
Snapctl commands for your snapend

#### 1. snapend help

See all the supported commands

```
# Help for the snapend command
snapctl snapend --help
```

#### 2. Snapend Downloads

Download Manifest, SDKs and Protos for your Snapend

```
# Help for the download command
snapctl snapend download --help

# Download your Snapend SDK and Protos
# $snapend_id = Cluster Id
# $category = snapend-manifest, client-sdk, server-sdk, protos
# $type = One of the supported types:
#   snapend-manifest(yaml, json)
#   client-sdk(unity, unreal, roblox, godot, cocos, ios-objc, ios-swift, android-java, android-kotlin, web-ts, web-js),
#   server-sdk(csharp, cpp, lua, ts, go, python, kotlin, java, c, node, js, perl, php, closure, ruby, rust),
#   protos(go, csharp, cpp, raw)
# $protos-category = messages or services (only with --type protos)
# $auth-type = user or app (only with --type server-sdk)
# Example:
# snapctl snapend download --snapend-id gx5x6bc0 --category snapend-manifest --type yaml --out-path .
# snapctl snapend download --snapend-id gx5x6bc0 --category sdk --type unity --sdk-access-type external --sdk-auth-type user --out-path .
# snapctl snapend download --snapend-id gx5x6bc0 --category sdk --type cpp --sdk-access-type internal --out-path .
# snapctl snapend download --snapend-id gx5x6bc0 --category protos --type raw --protos-category messages --out-path .
snapctl snapend download $snapend_id --category $category --type $type --sdk-access-type $sdk_access_type --sdk-auth-type $sdk_auth_type --out-path $out_path

```

#### 3. Clone Snapend

Clone a Snapend from an existing manifest. Passing the blocking flag ensures your CLI command waits till the new Snapend is up.

```
# Help for the clone command
snapctl snapend clone --help

# Clone your Snapend
# $gameId = Game Id
# $snapendName = Name of your new Snapend
# $env = One of development, staging
# $pathToManifest = Path to the manifest file; should include the file name
# Example:
# snapctl snapend clone --game-id 2581d802-aca-496c-8a76-1953ad0db165 --name new-snapend --env development --manifest-path "C:\Users\name\Downloads\snapser-ox1bcyim-manifest.json" --blocking
snapctl snapend clone --game-id $gameId --name $snapendName --env $env --manifest-path "$pathToManifest"
snapctl snapend clone --game-id $gameId --name $snapendName --env $env --manifest-path "$pathToManifest" --blocking
```

#### 4. Apply Snapend Changes

Apply changes to your Snapend from a manifest. You should have the latest manifest before applying changes. This is to prevent
a user stomping over someone elses changes. Passing the blocking flag ensures your CLI command waits till the update is complete.

```
# Help for the apply command
snapctl snapend apply --help

# Apply changes to a snapend via manifest
# $pathToManifest = Path to the manifest file; should include the file name
# Example:
# snapctl snapend apply --manifest-path "C:\Users\name\Downloads\snapser-ox1bcyim-manifest.json" --blocking
snapctl snapend apply --manifest-path "$pathToManifest"
snapctl snapend apply --manifest-path "$pathToManifest" --blocking
```

#### 5. Update Snapend BYOSnap or BYOGs versions

Update your BYOSnap or BYOGs versions for the Snapend

```
# Help for the byogs command
snapctl snapend update --help

# Update your Snapend with new BYOSnaps and BYOGs
# $snapend_id = Cluster Id
# $byosnaps = Comma separated list of BYOSnap ids and version.
# $byogs = Comma separated list of BYOGs fleet name, id and version.
# --blocking = (Optional) This makes sure the CLI waits till your Snapend is live.
# Note at least one of the two needs to be present
# Example:
# snapctl snapend update --snapend-id gx5x6bc0 --byosnaps byosnap-service-1:v1.0.0,byosnap-service--2:v1.0.0 --byogs byogs-fleet-one:gs-1:v0.0.1,my-fleet-two:gs-2:v0.0.4
# snapctl snapend update --snapend-id gx5x6bc0 --byosnaps byosnap-service-1:v1.0.0,byosnap-service--2:v1.0.0 --byogs fleet-one:v0.0.1,fleet-two:v0.0.4 --blocking
snapctl snapend update --snapend-id $snapend_id --byosnaps $byosnaps --byogs $byogs --blocking
```

#### 6. Get the Snapend state

Get the Snapend state

```
# Help for the byogs command
snapctl snapend state --help

# Get the Snapend state
# $snapend_id = Cluster Id
# Example:
# snapctl snapend state gx5x6bc0
snapctl snapend state $snapend_id
```

## Error codes
### CLI Return Codes
| Error Code | Description                                              |
|------------|----------------------------------------------------------|
| 0          | Operation completed successfully                         |
| 1          | General error                                            |
| 2          | Input error                                              |
| 3          | Resource not found                                       |

### Configuration Errors
| Error Code | Description                                              |
|------------|----------------------------------------------------------|
| 10         | Configuration incorrect                                  |
| 11         | Configuration error                                      |
| 12         | Dependency missing                                       |

### BYOGS Errors
| Error Code | Description                                              |
|------------|----------------------------------------------------------|
| 3          | BYOGs resource not found                                 |
| 20         | Generic BYOGS error                                      |
| 21         | BYOGS dependency missing                                 |
| 22         | BYOGS ECR login error                                    |
| 23         | BYOGS build error                                        |
| 24         | BYOGS tag error                                          |
| 25         | BYOGS publish error                                      |
| 26         | BYOGS publish permission error                           |
| 27         | BYOGS publish duplicate tag error                        |

### BYOSNAP Errors
| Error Code | Description                                              |
|------------|----------------------------------------------------------|
| 3          | BYOSnap resource not found                               |
| 30         | Generic BYOSNAP error                                    |
| 31         | BYOSNAP dependency missing                               |
| 32         | BYOSNAP ECR login error                                  |
| 33         | BYOSNAP build error                                      |
| 34         | BYOSNAP tag error                                        |
| 35         | BYOSNAP publish image error                              |
| 36         | BYOSNAP publish image permission error                   |
| 37         | BYOSNAP publish image duplicate tag error                |
| 38         | BYOSNAP create error                                     |
| 39         | BYOSNAP create permission error                          |
| 40         | BYOSNAP create duplicate name error                      |
| 41         | BYOSNAP publish version error                            |
| 42         | BYOSNAP publish version permission error                 |
| 43         | BYOSNAP publish version duplicate version error          |
| 44         | BYOSNAP publish version duplicate tag error              |
| 45         | BYOSNAP update version error                             |
| 46         | BYOSNAP update version service in use                    |
| 47         | BYOSNAP update version tag error                         |
| 48         | BYOSNAP update version invalid version error             |


### Game Errors
| Error Code | Description                                              |
|------------|----------------------------------------------------------|
| 3          | Game resource not found                                  |
| 50         | Generic game error                                       |
| 51         | Game create error                                        |
| 52         | Game create permission error                             |
| 53         | Game create limit error                                  |
| 54         | Game create duplicate name error                         |
| 55         | Game enumerate error                                     |

### Snapend Errors
| Error Code | Description                                              |
|------------|----------------------------------------------------------|
| 3          | Snapend resource not found                               |
| 60         | Generic snapend error                                    |
| 61         | Snapend enumerate error                                  |
| 62         | Snapend clone error                                      |
| 63         | Snapend clone server error                               |
| 64         | Snapend clone timeout error                              |
| 65         | Snapend apply error                                      |
| 66         | Snapend apply server error                               |
| 67         | Snapend apply timeout error                              |
| 68         | Snapend promote error                                    |
| 69         | Snapend promote server error                             |
| 70         | Snapend promote timeout error                            |
| 71         | Snapend download error                                   |
| 72         | Snapend update error                                     |
| 73         | Snapend update server error                              |
| 74         | Snapend update timeout error                             |
| 75         | Snapend state error                                      |

### Generate Errors
| Error Code | Description                                              |
|------------|----------------------------------------------------------|
| 80         | Generic generate error                                   |
| 81         | Generate profile error                                   |
| 82         | Generate credentials error                               |

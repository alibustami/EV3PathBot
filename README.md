# EV3PathBot

## Requirements

1- Conda
2- `Git bash` for Windows Users

## Usage

### Mac
#### Creating `Virtual Environment`

run this command:
```
$ make virenv
```

then activate the virtual environment
```
$ conda activate ev3pathbot-env
```

#### Install & build the package:
```
$ make install
```

### Windows
#### Creating `Virtual Environment`

run these commands in `git bash`:
```
$ cmake --build . --target virenv
```

then activate the virtual environment
```
$ conda activate ev3pathbot-env
```

#### Install & build the package:
```
$ cmake --build . --target install
```

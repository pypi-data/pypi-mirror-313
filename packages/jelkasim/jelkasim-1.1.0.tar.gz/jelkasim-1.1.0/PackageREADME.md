# Jelka simulation

```
usage: jelkasim [-h] [runner] target

Run jelka simulation.

positional arguments:
  runner      How to run your program.
  target      Your program name.

optional arguments:
  -h, --help  show this help message and exit
```

Examples:
```sh
jelkasim moj_vzorec.py
jelkasim moj_vzorec.exe
jelkasim node moj_vzorec.js
```

For ocaml inside docker something like this should be used (probably):
```sh
jelkasim docker exec container-name "ocaml moj_vzorec.ml"
```
You should also figure out the `container_name` using:
```sh
docker ps
```
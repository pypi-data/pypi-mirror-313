# Kaitai Struct: runtime library for Awkward

This library building Awkward Arrays using Kaitai Struct API for Awkward using
C++/STL.

## Steps

### 1. Write a .ksy file for your custom file format. Refer to the [Kaitai User Guide](https://doc.kaitai.io/user_guide.html) for more details.

Here, we take an example of `animal.ksy`

```yaml
meta:
  id: animal
  endian: le
  license: CC0-1.0
  ks-version: 0.8

seq:
  - id: entry
    type: animal_entry
    repeat: eos

types:
  animal_entry:
    seq:
      - id: str_len
        type: u1

      - id: species
        type: str
        size: str_len
        encoding: UTF-8

      - id: age
        type: u1

      - id: weight
        type: u2
```

### 2. Clone `kaitai_struct_awkward_runtime` repository:

```
git clone --recursive https://github.com/det-lab/kaitai_struct_awkward_runtime.git
```

```
cd kaitai_struct_awkward_runtime
```
```
git checkout ManasviGoyal/test
```

### 3. Update submodule and compile scala code (only the first time)

```
git submodule update --init
```

```
cd kaitai_struct_compiler
```

```
sbt package
```

```
cd ../
chmod u+x kaitai-struct-compiler
```

### 4. Generate the source and header files for Awkward target

```
./kaitai-struct-compiler -t awkward --outdir src-animal example_data/schemas/animal.ksy
```

### 5. Install the library
```
pip install awkward-kaitai
```

### 6. Build `awkward-kaitai` by passing the path of the main `.cpp` from the generated code.
If python gives a warning about the installation not being on the path, in order to get the file to build you may need to run:
```
echo "export PATH=$PATH:/whatever/path/python/says" >> ~/.bashrc
```

```
awkward-kaitai-build src-animal/animal.cpp -b build
```
> **Note:**
>
> `awkward-kaitai-build [-h] [-d DEST] [-b BUILD] file`
>
> options:
>- `-h, --help`: shows help message
>- `-d DEST, --dest DEST`: explicitly specify a destination for the build shared library.
>- `-b BUILD, --build BUILD`: explicitly specify a build location.

### 7. Open python and print the returned `ak.Array`:
```
python
```

```python
import awkward_kaitai

animal = awkward_kaitai.Reader("./src-animal/libanimal.so") # pass the path of the shared file
awkward_array = animal.load("example_data/data/animal.raw")

awkward_array.to_list()
```

#### Output

```python
[{'animalA__Zentry': [{'animal_entryA__Zstr_len': 3, 'animal_entryA__Zspecies': 'cat', 'animal_entryA__Zage': 5, 'animal_entryA__Zweight': 12}, {'animal_entryA__Zstr_len': 3, 'animal_entryA__Zspecies': 'dog', 'animal_entryA__Zage': 3, 'animal_entryA__Zweight': 43}, {'animal_entryA__Zstr_len': 6, 'animal_entryA__Zspecies': 'turtle', 'animal_entryA__Zage': 10, 'animal_entryA__Zweight': 5}]}]
```

## Related Papers and Talks
1. [Describe Data to get Science-Data-Ready Tooling: Awkward as a Target for Kaitai Struct YAML](https://indico.cern.ch/event/1330797/contributions/5796564/), Advanced Computing and Analysis Techniques for Physics Research Workshop 2024, New York, US.
2. [Awkward Target for Kaitai Struct](https://indico.cern.ch/event/1252095/contributions/5592420/), PyHEP Users Workshop 2023.

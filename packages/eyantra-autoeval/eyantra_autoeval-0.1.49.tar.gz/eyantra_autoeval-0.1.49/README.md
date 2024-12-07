# eyantra-autoeval

---
After changes, navigate to the "eyantra-autoeval" folder and do:
```sh
pip install .
```

## Usage

> NOTE: Check [#3][i3] for generating result from the evaluator.

- For `ROS2` mooc

  ```
  eyantra-autoeval evaluate --year 2024 --theme ROS --task 0
  ```

- For `Warehouse Drone` theme

  ```sh
  eyantra-autoeval evaluate --year 2024 --theme WD --task 0
  ```

- For `Logistic coBot` theme

  ```sh
  eyantra-autoeval evaluate --year 2024 --theme LB --task 0
  eyantra-autoeval evaluate --year 2024 --theme LB --task 1B
  eyantra-autoeval evaluate --year 2024 --theme LB --task 1C
  ```


- For `EcoMender Bot` theme

  ```sh
  eyantra-autoeval evaluate --year 2024 --theme EB --task 0
  eyantra-autoeval evaluate --year 2024 --theme EB --task 2A
  eyantra-autoeval evaluate --year 2024 --theme EB --task 2B
  ```

[i3]: https://github.com/eYantra-Robotics-Competition/eyantra-autoeval/issues/3

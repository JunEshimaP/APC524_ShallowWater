# APC524_ShallowWater

.github/workflows contains files concerning CI

src contains source code (such as __init__.py)

tests contains pytests to be run

.pre-commit-config.yaml does pre-commits

requirements.txt contains packages needed (to be used to note down packages being used for venv purposes)

#### 1D shallow water solver
+ Time: Euler forward
+ Space: 2nd order central difference
+ Initial shape: gaussian hump
+ Boundary contion: periodic 
+ Sample results:
![1Dwaves](https://user-images.githubusercontent.com/112533493/199803037-7f1f1281-0fbf-41f3-88d2-94902f751b8a.png)

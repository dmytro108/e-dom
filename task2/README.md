## Завдання 2
Побудуйте власну послідовність дій для двох логічних блоків та обґрунтуйте свій вибір. Об'єднайте деякі кроки разом, котрі вважаєте треба виконувати як один процесс у випадку ci-cd. Як результат отримати послідовність для майбутнього вибудовування ci-cd процесів для кожного з блоків.

**Блок 1**
- unit tests (quick)
- code linters
- publishing to environment
- build code
- integration tests (take a lot of time)
- docker image creating

**Блок 2**
- unit tests (quick)
- code linters
- release new package version in registry of packages
- build code
- create git tag for current branch
- publish static content for preview (static content is creating when run specific command for generate it)

## Рішення
Для зручності розділимо дії на дві групи - дії, що відносяться до CI і CD фаз. Це логічний поділ, який може не мати відображення в структурі пайплайна. 
Далі, об'єднаємо дії (steps) у стадії (stages). Цей поділ може бути відображено як stages і jobs у GitLabCI пайплайні. Для об'єднання дій у стадії, я керувався міркуваннями збереження гранулярності та, якщо можливо, паралельного виконання, як, наприклад, можна паралельно виконувати перевірку коду лінтерами та збірку коду.

**Блок 1**
- CI
  - stage: quality check
    - step: code linters
    - step: build code
  - steage: quick tests
    - step: unit tests
- CD
  - stage: publish
    - step: docker image creating
    - step: publishing to environment (staging)
  - stage: automation tests
    - step: integration tests

**Блок 2**
- CI
  - stage: quality check
    - step: code linters
    - step: build code
  - stage: quick test
    - step: unit tests
- CD
  - stage: publish static
    -  step: run specific command to generate static content
    -  step: publish static content for preview
  - stage: release
    - step: release new package version in registry of packages
    - step: create git tag for current branch
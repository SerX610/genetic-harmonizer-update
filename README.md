# Genetic Harmonizer Upgrade

This project has been developed by **_Sergio Cárdenas Gracia_** & **_Siddharth Saxena_** in the context of the Valerio Velardo's "Computational Music Creativity" course from the Master in Sound and Music Computing at Universitat Pompeu Fabra. For more information, refer to the [Assigment.md](Assignment.md) file.

The goal of this project is to re-adapt a genetic algorithm model (based on the Valerio's [script](https://github.com/musikalkemist/generativemusicaicourse/blob/main/16.%20Melody%20harmonization%20with%20genetic%20algorithms/Code/geneticmelodyharmonizer.py)) to harmonize a melody in a jazz style.


## Setup

- Clone the repository.

- Install the project dependencies using the following command:

```bash
>>> pip install -r requirements.txt
```


## Usage

To harmonize a melody using the jazz genetic algorithm, run:

```bash
>>> python geneticmelodyjazzharmonizer.py
```

This will generate a jazz-style harmonization for the input melody and automatically open a MuseScore file containing the original melody and the generated jazz chord sequence.


## How it works

The `geneticmelodyjazzharmonizer.py` script harmonizes a given melody using a genetic algorithm. The process relies on the following core components:

- `MelodyData` class: Represents the data of a melody, including its notes, total duration, and the number of bars.

- `GeneticMelodyHarmonizer` class: This is the main class handling the genetic algorithm process, including initialization, evolution, and final harmonization output.

- `FitnessEvaluator` class: Evaluates the fitness of a chord sequence based on various musical criteria.

- `create_score` function: Create a music21 score with a given melody and chord sequence.


## Jazz Fitness Metrics

The fitness function evaluates harmonizations based on jazz harmony principles. It uses various metrics, which are defined in an object-oriented manner within the `metrics.py` file. That is, each metric is a subclass of the abstract `Metric` class, making it easy to add new metrics if needed.

#### Implemented Metrics

The algorithm assumes two chords per bar, with notes ranging from `C4` to `B4`. The following metrics are used:

- **Chord-Melody Congruence**: Measures how well melody notes fit within the generated chords. Higher scores when melody notes are present in the corresponding chords.

- **Chord Variety**: Encourages harmonic diversity. Higher scores for sequences with more unique chords.

- **Harmonic Flow**: Evaluates chord transitions based on the given preferred transitions. Rewards smooth and musically logical chord changes.

- **Functional Harmony**: Checks for key harmonic structures. Ensures the presence of tonic, subdominant, and dominant chords.

- **Voice Leading**: Evaluates smoothness in note transitions between chords. Rewards minimal leaps and common tone retention.

- **Chord Repetitions**: Encourages variation while allowing some stability. Penalizes excessive repetition of the same chord.

- **Functional Progressions**: Checks for given jazz-standard progressions (e.g., ii-V-I). Rewards sequences that follow established harmonic movements.

- **Non-Diatonic Chords**: Encourages the use of non-diatonic chords. Rewards chromaticism and harmonic color.

- **Parallel Fifths**: Penalizes parallel fifths. Discourages parallel movement of perfect fifths between chords.

Each metric is weighted according to the `weights` dictionary in `geneticmelodyjazzharmonizer.py`. 


## Observations

The current implementation achieves promising harmonization results, but balancing the metric weights is a complex task. Thus, further experimentation is encouraged. For that, consider fine-tunning metric weights, introducing new metrics, or expanding the chord set.
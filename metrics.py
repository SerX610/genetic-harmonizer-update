from abc import ABC, abstractmethod


class Metric(ABC):
    """
    Abstract base class for musical metrics.
    Any metric class must implement the `calculate` method.
    """
    def __init__(self):
        pass

    @abstractmethod
    def calculate(self, chord_sequence):
        """
        Calculate the metric score for a given chord sequence.
        
        Parameters:
            chord_sequence (list): A list of chords to be evaluated.
        
        Returns:
            float: A score representing the evaluated metric.
        """
        pass


class ChordMelodyCongruence(Metric):
    """
    Calculates the congruence between the chord sequence and the melody.
    This class assesses how well each chord in the sequence aligns with
    the corresponding segment of the melody. The alignment is measured 
    by checking if the notes in the melody are present in the chords 
    being played at the same time, rewarding sequences where the melody 
    notes fit well with the chords.

    Parameters:
        melody_data (MelodyData): Melody information.
        chord_mappings (dict): Available chords mapped to their notes.
    """
    def __init__(self, melody_data, chord_mappings):
        self.melody_data = melody_data
        self.chord_mappings = chord_mappings

    def calculate(self, chord_sequence):
        score, melody_index = 0, 0
        for chord in chord_sequence:
            bar_duration = 0
            while bar_duration < 4 and melody_index < len(self.melody_data.notes):
                pitch, duration = self.melody_data.notes[melody_index]
                if pitch[0] in self.chord_mappings[chord]:
                    score += duration
                bar_duration += duration
                melody_index += 1
        return score / self.melody_data.duration


class ChordVariety(Metric):
    """
    Evaluates the diversity of chords used in the sequence. This class
    calculates a score based on the number of unique chords present in the
    sequence compared to the total available chords. Higher variety in the
    chord sequence results in a higher score, promoting musical
    complexity and interest.

    Parameters:
        chord_mappings (dict): Available chords mapped to their notes.
    """
    def __init__(self, chord_mappings):
        self.chord_mappings = chord_mappings

    def calculate(self, chord_sequence):
        unique_chords = len(set(chord_sequence))
        total_chords = len(self.chord_mappings)
        return unique_chords / total_chords


class HarmonicFlow(Metric):
    """
    Assesses the harmonic flow of the chord sequence by examining transitions.
    This class scores the sequence based on how frequently the chord
    transitions align with predefined preferred transitions. Smooth and
    musically pleasant transitions result in a higher score.

    Parameters:
        preferred_transitions (dict): Preferred chord transitions.
    """
    def __init__(self, preferred_transitions):
        self.preferred_transitions = preferred_transitions

    def calculate(self, chord_sequence):
        score = 0
        total_transitions = len(chord_sequence) - 1
        correct_transition_score = 1 / total_transitions
        for i in range(total_transitions):
            next_chord = chord_sequence[i + 1]
            if next_chord in self.preferred_transitions[chord_sequence[i]]:
                score += correct_transition_score
        return score


class FunctionalHarmony(Metric):
    """
    Evaluates the chord sequence based on principles of functional harmony.
    This class checks for the presence of key harmonic functions such as
    the tonic at the beginning and end of the sequence and the presence of
    subdominant and dominant chords. Adherence to these harmonic
    conventions is rewarded with a higher score.
    """
    def calculate(self, chord_sequence):
        score = 0
        total_rules = 3
        correct_function_score = 1 / total_rules
        if chord_sequence[0] in ["Cmaj7", "Fmaj7"]:
            score += correct_function_score
        if chord_sequence[-1] in ["Cmaj7"]:
            score += correct_function_score
        if "Fmaj7" in chord_sequence and "G7" in chord_sequence:
            score += correct_function_score
        return score


class VoiceLeading(Metric):
    """
    Evaluates the chord sequence based on movement between successive
    chords. This class scores the sequence based on how smoothly the
    notes in the chords move from one to the next. Smooth voice leading
    results in a higher score. This class can be used to encourage
    more natural and melodic chord progressions.

    Parameters:
        chord_mappings (dict): Available chords mapped to their notes.
    """
    def __init__(self, chord_mappings):
        self.chord_mappings = chord_mappings

    def calculate(self, chord_sequence):
        score = 0
        total_transitions = len(chord_sequence) - 1
        total_notes = 4 * total_transitions
        shared_note_score = 1 / total_notes
        for i in range(total_transitions):
            current_chord = self.chord_mappings[chord_sequence[i]]
            next_chord = self.chord_mappings[chord_sequence[i + 1]]
            for note in current_chord:
                if note in next_chord:
                    score += shared_note_score
        return score
    

class ChordRepetitions(Metric):
    """
    Evaluates the chord sequence based on the presence of repeated chords.
    This class checks for the occurrence of repeated chords in the
    sequence. Repeated chords can add stability and structure to a
    progression, but excessive repetition can lead to monotony. This
    class penalizes sequences with repeated chords.

    Parameters:
    """
    def calculate(self, chord_sequence):
        score = 1
        total_transitions = len(chord_sequence) - 2
        same_chord_penalty = - 1 / total_transitions
        for i in range(total_transitions):
            if chord_sequence[i] == chord_sequence[i + 1]:
                score += same_chord_penalty
            if chord_sequence[i] == chord_sequence[i + 2]:
                score += same_chord_penalty
        return score


class FunctionalProgressions(Metric):
    """
    Evaluates the chord sequence based on the presence of common functional
    jazz progressions. This class checks for the occurrence of common
    chord progressions such as the ii-V-I progression. The presence of
    these progressions is rewarded with a higher score, promoting the use
    of well-established harmonic movements.

    Parameters:
        common_progressions (list): Common functional chord progressions.
    """
    def __init__(self, common_progressions):
        self.common_progressions = common_progressions

    def calculate(self, chord_sequence):
        score = 0
        total_transitions = len(chord_sequence) - 2
        common_progression_score = 3 / (total_transitions)
        for i in range(total_transitions):
            if chord_sequence[i:i+3] in self.common_progressions:
                score += common_progression_score
        return score


class NonDiatonicChords(Metric):
    """
    Evaluates the chord sequence based on the use of non-diatonic chords.
    This class checks for the presence of non-diatonic chords that are
    not part of the key of C major. Non-diatonic chords can introduce
    tension and color to a harmonic progression. This function rewards
    sequences that include these non-diatonic chords.
    """
    def calculate(self, chord_sequence):
        score = 0
        total_chords = len(chord_sequence)
        non_diationic_chord_score = 1 / total_chords
        non_diatonic_chords = {"C7", "D7", "E7", "A7", "Dm7b5", "Eº7", "Gmin7"}
        for chord in chord_sequence:
            if chord in non_diatonic_chords:
                score += non_diationic_chord_score
        return score
        

class ParallelFifths(Metric):
    """
    Evaluates the chord sequence based on the presence of parallel fifths.
    This class checks for the occurrence of parallel fifths between
    successive chords in the sequence. Parallel fifths can create a
    specific harmonic effect that may or may not be desired in a jazz
    context. This class penalizes sequences with parallel fifths.

    Parameters:
        chords_with_parallel_fifths (set): Chords with parallel fifths.
    """
    def __init__(self, chords_with_parallel_fifths):
        self.chords_with_parallel_fifths = chords_with_parallel_fifths

    def calculate(self, chord_sequence):
        score = 1
        total_transitions = len(chord_sequence) - 1
        parallel_fifth_penalty = - 1 / total_transitions
        for i in range(total_transitions):
            if frozenset([chord_sequence[i], chord_sequence[i + 1]]
                         ) in self.chords_with_parallel_fifths:
                score += parallel_fifth_penalty
        return score

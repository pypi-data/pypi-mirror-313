import math
import random
from collections import Counter


class ListWizard:
    # 1. Statistics
    @staticmethod
    def calculate_statistics(numbers):
        if not numbers:
            raise ValueError("The list is empty.")

        n = len(numbers)
        sorted_numbers = sorted(numbers)
        mean = sum(numbers) / n
        median = sorted_numbers[n // 2] if n % 2 else (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
        mode = Counter(numbers).most_common(1)[0][0]
        data_range = max(numbers) - min(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / n
        std_dev = math.sqrt(variance)

        return {
            "sum": sum(numbers),
            "mean": mean,
            "median": median,
            "mode": mode,
            "range": data_range,
            "variance": variance,
            "std_dev": std_dev,
        }

    # 2. Element Frequency
    @staticmethod
    def element_frequency(lst):
        return dict(Counter(lst))

    # 3. List Similarity
    @staticmethod
    def list_similarity(list1, list2):
        common_elements = set(list1).intersection(list2)
        total_elements = set(list1).union(list2)
        similarity = (len(common_elements) / len(total_elements)) * 100
        return similarity

    # 4. Filter & Transform
    @staticmethod
    def filter_transform(lst, filter_func=None, transform_func=None):
        if filter_func:
            lst = filter(filter_func, lst)
        if transform_func:
            lst = map(transform_func, lst)
        return list(lst)

    # 5. Sorting
    @staticmethod
    def sort_list(lst, key=None, reverse=False):
        return sorted(lst, key=key, reverse=reverse)

    # 6. Shuffling
    @staticmethod
    def shuffle_list(lst):
        shuffled = lst[:]
        random.shuffle(shuffled)
        return shuffled

    # 7. Unique List Generator
    @staticmethod
    def unique_list(lst):
        seen = set()
        return [x for x in lst if not (x in seen or seen.add(x))]

    # 8. Insertion
    @staticmethod
    def insert_at(lst, element, position):
        return lst[:position] + [element] + lst[position:]

    # 9. Circular Shift
    @staticmethod
    def circular_shift(lst, shift):
        shift %= len(lst)
        return lst[-shift:] + lst[:-shift]

    # 10. List Merging
    @staticmethod
    def merge_lists(*lists):
        merged = []
        for lst in lists:
            merged.extend(lst)
        return ListWizard.unique_list(merged)

    # 11. List to String
    @staticmethod
    def list_to_string(lst, separator=", "):
        return separator.join(map(str, lst))

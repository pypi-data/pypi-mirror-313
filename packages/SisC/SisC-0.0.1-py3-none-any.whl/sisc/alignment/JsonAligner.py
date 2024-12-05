from typing import List, Optional, Any
from sisc.alignment.BaseFileAligner import BaseFileAligner


class JsonAligner(BaseFileAligner[Any]):

    def __init__(self, keys_to_update: Optional[List[str]]=None):
        if keys_to_update is None:
            keys_to_update = ['start', 'end']
        self.keys_to_update = keys_to_update

    # overriding abstract method
    def align(self, input_content: Any, aligned_text: str, aligned_fingerprint: str, text_gap_positions: List[int],
              fingerprint_gap_positions: List[int]) -> Any:
        """
        TBD
        :param input_content:
        :param aligned_text:
        :param aligned_fingerprint:
        :param text_gap_positions:
        :param fingerprint_gap_positions:
        :return:
        """
        json_output = self.__update_json(input_content, fingerprint_gap_positions, '')
        return json_output

    def __update_json(self, json_obj: Any, fingerprint_gap_positions: List[int], prefix: str) -> Any:
        result: Any = None

        if isinstance(json_obj, dict):
            result = {}

            for key, value in json_obj.items():

                if isinstance(value, dict) or isinstance(value, list):
                    sub_prefix = prefix

                    if sub_prefix:
                        sub_prefix += '.'
                    sub_prefix += f'{key}'

                    if isinstance(value, dict):
                        child = self.__update_json(value, fingerprint_gap_positions, sub_prefix)
                    else:
                        child = self.__update_json(value, fingerprint_gap_positions, sub_prefix)
                else:
                    need_update = self.__need_update(key, prefix)
                    if need_update:
                        child = self.__calculate_new_value(value, fingerprint_gap_positions)
                    else:
                        child = value

                result[key] = child

        elif isinstance(json_obj, list):
            result = []

            for value in json_obj:
                if isinstance(value, dict):
                    child = self.__update_json(value, fingerprint_gap_positions, prefix)
                else:
                    child = value

                result.append(child)

        return result

    def __need_update(self, key: str, prefix: str) -> bool:
        update = False
        for full_key_to_update in self.keys_to_update:
            parts = full_key_to_update.rsplit('.', 1)

            if len(parts) == 2:
                key_prefix = parts[0]
                key_suffix = parts[1]

                if key_prefix == prefix and key_suffix == key:
                    update = True
                    break
            else:
                if full_key_to_update == key:
                    update = True
                    break

        return update

    def __calculate_new_value(self, value: int, fingerprint_gap_positions: List[int]) -> int:
        count_before = self.__count_before(value, fingerprint_gap_positions)
        cur_value = value
        found_gap = True
        while found_gap:
            if cur_value in fingerprint_gap_positions:
                cur_value += 1
            else:
                found_gap = False

        return cur_value + count_before

    @staticmethod
    def __count_before(value: int, gap_positions: List[int]) -> int:
        count_before = 0
        for pos in gap_positions:
            if pos < value + count_before:
                count_before += 1
            else:
                break

        return count_before

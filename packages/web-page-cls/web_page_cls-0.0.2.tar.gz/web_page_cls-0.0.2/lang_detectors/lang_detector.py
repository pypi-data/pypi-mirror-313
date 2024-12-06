"""
Language identification
"""
import os
import time

import pandas as pd
from huggingface_hub import hf_hub_download

from lang_detectors.fasttext_custom import load_model
from lang_detectors.json_loader import load_json, save_json


class LanguageIdentificator:
    """
    Language identification based on FastText. Supports 173 languages
    """

    def __init__(self, use_hf_model=False) -> None:
        """
            use_hf_model (bool, optional): load model from hugging face. 
            HF model slower. Quality need to be tested


        """
        self.use_hf_model = use_hf_model

        if use_hf_model:
            self.model_path = hf_hub_download(
                repo_id="facebook/fasttext-language-identification", filename="model.bin")

            self.model = load_model(self.model_path)
        else:

            self.model_path = os.path.join(
                os.path.dirname(__file__), 'lid.176.bin')
            self.model = load_model(self.model_path)

        self.iso_path = os.path.join(
            os.path.dirname(__file__), 'iso-639-3.tab')
        self.code2lang_path = os.path.join(
            os.path.dirname(__file__), 'code2lang.json')

        self.code2lang = self.get_code2lang_dict()

    def predict(self, text: str):
        """
        Predict language. Supports 173 languages
        """

        text = self.clear_text(text)

        if self.use_hf_model:
            result = self.model.predict(text)
        else:
            result = self.model.predict(text)

        # result look like  (('__label__ru',), array([0.99998832]))

        return {'label': self.delete_thunders_from_label(result[0][0]), 'prob': float(result[1][0])}

    def clear_text(self, text: str) -> str:
        """
        Remove bad characters from text
        """
        splitted_text = text.split('\n')
        cleaned_text = ' '.join(splitted_text)

        return cleaned_text

    def delete_thunders_from_label(self, label: str) -> str:
        """
        '__label__ru' -> 'ru'
        """
        return label.split('__label__')[-1]

    def get_code2lang_dict(self):
        """
        Return dict like
            {
                'pt' : 'Portuguese',
                'ro' : 'Romanian',
                'ru' : 'Russian'
            }
        Contains 173 languages
        """

        if os.path.exists(self.code2lang_path):
            return load_json(self.code2lang_path)

        code2lang = self.get_iso_dict()
        save_json(code2lang, self.code2lang_path)

        return code2lang

    def get_iso_dict(self):
        """
        Convert lang short code to language
        For example:
            pt -> Portuguese
            ro -> Romanian
            ru -> Russian
        """

        codes = 'af als am an ar arz as ast av az azb ba bar bcl be bg bh bn bo bpy br bs bxr ca cbk ce ceb ckb co cs cv cy da de diq dsb dty dv el eml en eo es et eu fa fi fr frr fy ga gd gl gn gom gu gv he hi hif hr hsb ht hu hy ia id ie ilo io is it ja jbo jv ka kk km kn ko krc ku kv kw ky la lb lez li lmo lo lrc lt lv mai mg mhr min mk ml mn mr mrj ms mt mwl my myv mzn nah nap nds ne new nl nn no oc or os pa pam pfl pl pms pnb ps pt qu rm ro ru rue sa sah sc scn sco sd sh si sk sl so sq sr su sv sw ta te tg th tk tl tr tt tyv ug uk ur uz vec vep vi vls vo wa war wuu xal xmf yi yo yue zh'
        codes = codes.split(' ')

        df = pd.read_csv(self.iso_path, sep='\t')

        code2lang = {}

        for code in codes:
            name = df[(df['Id'].str.strip() == code) |
                      (df['Part1'].str.strip() == code)]

            if not name.empty:
                code2lang[code] = name['Ref_Name'].iloc[0]

        return code2lang


if __name__ == '__main__':
    from colorama import Fore, Style
    from colorama import init as colorama_init

    colorama_init()

    test_text = """Удары пришлись как раз во время швартовки одного из паромов. 
    Румынская сторона открыла огонь по русским БПЛА, но неудачно. В результате взрыва поврежден сам терминал и один из паромов. Уничтожена техника, и была слышна мощная детонация боекомплекта. Раненых и погибших эвакуировали на румынскую территорию пограничными катерами", — отметил Лебедев. В ответ на атаки ВСУ по гражданским объектам российские войска регулярно наносят прицельные удары по местам расположения личного состава, техники и наемников, а также по инфраструктуре: объектам энергетики, оборонной промышленности, военного управления и связи Украины. При этом пресс-секретарь президента Дмитрий Песков не раз подчеркивал, что армия не бьет по жилым домам и социальным учреждениям."""

    detector_fasttext = LanguageIdentificator(use_hf_model=False)
    detector_hf = LanguageIdentificator(use_hf_model=True)

    for det in [detector_fasttext, detector_hf]:
        start = time.time()
        print(f'\n{Fore.MAGENTA}label: {Fore.YELLOW}{det.predict(test_text)}.{Fore.MAGENTA}Time spent: {Fore.YELLOW}{time.time() - start: 0.6f} sec')

# Source Generated with Decompyle++
# File: thesaurus.pyc (Python 3.11)

'''
近义词知识库模块
用于管理和处理近义词及相关知识
'''
import os
import json

class Thesaurus:
    '''近义词知识库类'''

    def __init__(self):
        '''初始化近义词知识库'''
        self.thesaurus_file = os.path.join(os.path.dirname(__file__), 'thesaurus.json')
        self.default_thesaurus = {
            '文档': {
                'synonyms': [
                    '文件',
                    '文稿',
                    '资料',
                    '文本'],
                'knowledge': '文档是记录信息的载体，包括电子文档和纸质文档，常用于办公和信息传递。' },
            '报告': {
                'synonyms': [
                    '汇报',
                    '总结',
                    '简报'],
                'knowledge': '报告是向上级或相关方汇报工作或情况的书面材料，通常包含数据、分析和建议。' },
            '计划': {
                'synonyms': [
                    '规划',
                    '方案',
                    '安排'],
                'knowledge': '计划是对未来工作的安排和部署，包括目标、步骤、资源分配等。' },
            '图片': {
                'synonyms': [
                    '照片',
                    '图像',
                    '相片'],
                'knowledge': '图片是通过摄影、绘画等方式形成的视觉资料，常用于直观展示信息。' },
            '视频': {
                'synonyms': [
                    '影片',
                    '影像'],
                'knowledge': '视频是由连续的图像帧组成的动态视觉资料，常用于记录和传播动态信息。' },
            '音频': {
                'synonyms': [
                    '声音',
                    '音效'],
                'knowledge': '音频是通过录音设备记录的声音信号，常用于传播语音、音乐等信息。' },
            '数据': {
                'synonyms': [
                    '信息',
                    '资料'],
                'knowledge': '数据是描述客观事物的符号和载体，常用于分析和决策支持。' },
            '表格': {
                'synonyms': [
                    '表单',
                    '数据表'],
                'knowledge': '表格是用于整理和展示数据的结构化格式，常用于数据对比和统计。' },
            '演示': {
                'synonyms': [
                    '展示',
                    '宣讲'],
                'knowledge': '演示是向他人展示产品或方案的过程，常用于推广和培训。' },
            '会议': {
                'synonyms': [
                    '会面',
                    '会商'],
                'knowledge': '会议是多人聚集讨论问题或进行决策的活动，常用于团队协作和沟通。' } }
        self.load_thesaurus()


    def load_thesaurus(self):
        '''从文件加载近义词库'''
        try:
            if os.path.exists(self.thesaurus_file):
                with open(self.thesaurus_file, 'r', encoding='utf-8') as f:
                    self.thesaurus = json.load(f)
            else:
                self.thesaurus = self.default_thesaurus
                self.save_thesaurus()
        except (IOError, json.JSONDecodeError):
            self.thesaurus = self.default_thesaurus


    def save_thesaurus(self):
        '''将近义词库保存到文件'''
        try:
            with open(self.thesaurus_file, 'w', encoding='utf-8') as f:
                json.dump(self.thesaurus, f, ensure_ascii=False, indent=4)
        except IOError:
            pass

    def get_synonyms(self, word):
        '''
        获取单词的所有近义词（包括单词本身）

        Args:
            word: 要查找的单词

        Returns:
            list: 包含单词本身和所有近义词的列表
        '''
        lower_word = word.lower()
        synonyms = set()
        synonyms.add(word)
        for key, data in self.thesaurus.items():
            lower_key = key.lower()
            if lower_key == lower_word:
                synonyms.update(data['synonyms'])
                synonyms.add(key)

            lower_values = [s.lower() for s in data.get('synonyms', [])]
            if lower_word in lower_values:
                synonyms.add(key)
                synonyms.update(data['synonyms'])
        return list(synonyms)


    def get_knowledge(self, word):
        """
        获取单词的相关知识

        Args:
            word: 要查找的单词

        Returns:
            dict: 包含单词和相关知识的字典，格式为{'word': str, 'knowledge': str, 'synonyms': list}，如果没有则返回None
        """
        lower_word = word.lower()
        for key, data in self.thesaurus.items():
            lower_key = key.lower()
            if lower_key == lower_word:
                return {
                    'word': key,
                    'knowledge': data.get('knowledge', ''),
                    'synonyms': data.get('synonyms', [])
                }
            lower_values = [s.lower() for s in data.get('synonyms', [])]
            if lower_word in lower_values:
                return {
                    'word': key,
                    'knowledge': data.get('knowledge', ''),
                    'synonyms': data.get('synonyms', [])
                }
        return None


    def add_synonyms(self, word, synonyms, knowledge, bidirectional=True):
        '''
        添加近义词到知识库中

        Args:
            word: 基础词
            synonyms: 近义词列表
            knowledge: 相关知识，默认为空字符串
            bidirectional: 是否创建双向映射，默认为True
        '''
        if word not in self.thesaurus:
            self.thesaurus[word] = {'synonyms': [], 'knowledge': ''}

        self.thesaurus[word]['synonyms'].extend(s for s in synonyms if s not in self.thesaurus[word]['synonyms'])
        if knowledge:
            self.thesaurus[word]['knowledge'] = knowledge

        if bidirectional:
            for s in synonyms:
                if s not in self.thesaurus:
                    self.thesaurus[s] = {'synonyms': [], 'knowledge': ''}
                if word not in self.thesaurus[s]['synonyms']:
                    self.thesaurus[s]['synonyms'].append(word)

        self.save_thesaurus()


    def update_synonyms(self, old_word, new_word, new_synonyms, knowledge, bidirectional=True):
        '''
        更新近义词条目

        Args:
            old_word: 原基础词
            new_word: 新基础词
            new_synonyms: 新近义词列表
            knowledge: 相关知识，默认为空字符串
            bidirectional: 是否创建双向映射，默认为True
        '''
        self.remove_word(old_word)
        self.add_synonyms(new_word, new_synonyms, knowledge, bidirectional)


    def remove_word(self, word):
        '''
        从近义词库中移除单词

        Args:
            word: 要移除的单词
        '''
        if word in self.thesaurus:
            synonyms = self.thesaurus[word]['synonyms']
            del self.thesaurus[word]
            for s in synonyms:
                if s in self.thesaurus and word in self.thesaurus[s]['synonyms']:
                    self.thesaurus[s]['synonyms'].remove(word)

        self.save_thesaurus()


    def show_thesaurus(self):
        '''显示近义词库内容'''
        if not self.thesaurus:
            print('近义词库为空')
            return
        for word, data in self.thesaurus.items():
            print(f'''{word}:''')
            print(f'''  近义词: {', '.join(data['synonyms'])}''')
            print(f'''  相关知识: {data.get('knowledge', '')}''')

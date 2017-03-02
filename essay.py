import os
import time
import re

class Essay(object):

    def __init__(self, id, title='', categories='', tags='', content=''):
        self.id = id
        self.path = 'source/essays/{id}'.format(id=self.id)
        self.meta_path = '{path}/{id}_meta.md'.format(path=self.path, id=self.id)
        self.body_path = '{path}/{id}_body.md'.format(path=self.path, id=self.id)

        if os.path.exists(self.path):
            if len(title + categories + tags + content) > 0:
                print('{id}文档已存在，多余参数将被忽略'.format(id=self.id))
            self.update_from_files()
        else:
            os.mkdir(self.path)
            self.init_new(title, categories, tags, content)

    def update_from_files(self):
        with open(self.meta_path, 'r', encoding='utf-8') as meta_file:
            self.meta = '\n'.join(
                [line.strip('\n') for line in meta_file.readlines() if len(line) > 0]
            )
        self.title = re.search(r'title:(.*?)\n', self.meta).group().strip()
        self.date = re.search(r'date:(.*?)\n', self.meta).group().strip()
        self.categories = re.search(r'categories:(.*?)\n', self.meta).group().strip()
        self.tags = re.search(r'tags:(.*?)\n', self.meta).group().strip()
        with open(self.body_path, 'r', encoding='utf-8') as body_file:
            self.body = body_file.read()

    def init_new(self, title='', categories='', tags='', content=''):
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.title = title
        self.categories = categories
        self.tags = tags

        self.meta = '\n'.join([line.strip() for line in '''
         ---
         title: {t}
         date: {d}
         categories: {c}
         tags: {ts}
         ---'''.format(
            t=self.title, d=self.date, c=self.categories, ts=self.tags
        ).split('\n') if len(line) > 0])

        self.body = '# {title}'.format(title=self.title) + content

        with open(self.meta_path, 'w', encoding='utf-8') as meta_file:
            meta_file.write(self.meta)
        with open(self.body_path, 'w', encoding='utf-8') as body_file:
            body_file.write(self.body)

    def pub2hexo(self):
        self.hexo_path = 'public/hexo/{id}.md'.format(id=self.id)
        with open(self.hexo_path, 'w', encoding='utf-8') as hexo_file:
            hexo_file.write(self.meta + '\n\n' + self.body)
        print('适合Hexo发布的文档成功保存在{path}'.format(path=self.hexo_path))

    def pub2gitbook(self):
        pass

    def pub2weixin(self):
        pass

    def pub2zhihu(self):
        pass

    def pub2jianshu(self):
        pass

    def pub2douban(self):
        pass

    def pub2docx(self):
        pass

if __name__ == '__main__':

    essay = Essay('test_essay', '测试文章')
    essay.pub2hexo()
import re
import time
import hashlib
import bibtexparser
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import OrderedDict, Counter
from typing import List, Dict, Tuple
import glob

# 获取脚本实际位置
SCRIPT_DIR = Path(__file__).parent.absolute()

class BibReferenceManager:
    def __init__(self, tex_file, bib_file):
        self.tex_file = Path(tex_file).absolute()
        self.bib_file = Path(bib_file).absolute()
        self.cite_commands = [
            r'\\cite\{([^}]+)\}',
            r'\\citep\{([^}]+)\}',
            r'\\citet\{([^}]+)\}',
            r'\\citealp\{([^}]+)\}',
            r'\\citealt\{([^}]+)\}',
            r'\\citeyear\{([^}]+)\}',
            r'\\citeyearpar\{([^}]+)\}',
            r'\\citeauthor\{([^}]+)\}',
            r'\\textcite\{([^}]+)\}',
            r'\\parencite\{([^}]+)\}',
            r'\\autocite\{([^}]+)\}',
            r'\\footcite\{([^}]+)\}',
            r'\\nocite\{([^}]+)\}'
        ]
        self.last_citations_hash = None
        
    def get_tex_content(self) -> str:
        """读取tex文件内容"""
        try:
            with open(self.tex_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading tex file: {e}")
            return ""

    def get_citations_from_content(self, content: str) -> Tuple[List[str], Dict[str, int]]:
        citations_ordered = OrderedDict()
        citations_count = Counter()
        citations_context = {}
        
        # 首先遍历一次确定每个引用的首次出现顺序
        first_appearances = {}  # 新增：记录每个引用的首次出现顺序
        citation_number = 1     # 新增：引用编号计数器
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('%'):
                continue
                
            for pattern in self.cite_commands:
                matches = re.finditer(pattern, line)
                for match in matches:
                    start_pos = match.start()
                    
                    comment_pos = line.find('%', 0, start_pos)
                    if comment_pos != -1:
                        continue
                        
                    cite_group = match.group(1)
                    for citation in cite_group.split(','):
                        citation = citation.strip()
                        if citation and citation not in first_appearances:
                            first_appearances[citation] = citation_number
                            citation_number += 1

        # 第二次遍历收集所有引用信息
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('%'):
                continue
                
            for pattern in self.cite_commands:
                matches = re.finditer(pattern, line)
                for match in matches:
                    start_pos = match.start()
                    
                    comment_pos = line.find('%', 0, start_pos)
                    if comment_pos != -1:
                        continue
                        
                    cite_group = match.group(1)
                    for citation in cite_group.split(','):
                        citation = citation.strip()
                        if citation:
                            if citation not in citations_ordered:
                                citations_ordered[citation] = len(citations_ordered)
                                
                            context_start = max(0, start_pos - 5)
                            context_end = min(len(line), start_pos + len(match.group(0)) + 5)
                            context = line[context_start:context_end]
                            
                            if citation not in citations_context:
                                citations_context[citation] = []
                            citations_context[citation].append({
                                'line_number': line_num,
                                'context': context,
                                'citation_number': first_appearances[citation]  # 修改：使用首次出现的编号
                            })
                            
                            citations_count[citation] += 1

        citation_stats = {
            citation: {
                'order': order,
                'count': citations_count[citation],
                'contexts': citations_context[citation],
                'citation_number': first_appearances[citation]  # 新增：保存固定的引用编号
            }
            for citation, order in citations_ordered.items()
        }

        return list(citations_ordered.keys()), citation_stats

    def process_bib_file(self) -> tuple:
        """处理bib文件并重组引用"""
        content = self.get_tex_content()
        citations, citation_stats = self.get_citations_from_content(content)
        
        try:
            with open(self.bib_file, 'r', encoding='utf-8') as f:
                bib_database = bibtexparser.load(f)
        except Exception as e:
            print(f"Error reading bibliography file: {e}")
            return 0, 0

        all_entries = {entry['ID']: entry for entry in bib_database.entries}
        
        cited_entries = []
        uncited_entries = []
        cited_keys = set()

        for citation in citations:
            if citation in all_entries:
                entry = all_entries[citation].copy()
                entry['citation_count'] = citation_stats[citation]['count']
                entry['first_appearance'] = citation_stats[citation]['order']
                entry['contexts'] = citation_stats[citation]['contexts']  # 新增：添加上下文信息
                cited_entries.append(entry)
                cited_keys.add(citation)
            else:
                print(f"Warning: Citation '{citation}' not found in bibliography")

        for entry_id, entry in all_entries.items():
            if entry_id not in cited_keys:
                entry_copy = entry.copy()
                entry_copy['citation_count'] = 0
                uncited_entries.append(entry_copy)

        self._save_organized_entries(cited_entries, uncited_entries)
        return len(cited_entries), len(uncited_entries)
    
    def generate_citation_report(self, cited_entries: List[Dict]) -> str:
        """生成引用统计报告"""
        report = []
        report.append("="*50)
        report.append("Citation Statistics Report")
        report.append("="*50)
        
        # 基本统计
        total_citations = sum(entry['citation_count'] for entry in cited_entries)
        report.append(f"\n1. Basic Statistics:")
        report.append(f"   - Total unique references: {len(cited_entries)}")
        report.append(f"   - Total citations: {total_citations}")
        report.append(f"   - Average citations per reference: {total_citations/len(cited_entries):.2f}")
        
        # 最常引用的文献
        report.append(f"\n2. Most Cited References:")
        sorted_entries = sorted(cited_entries, key=lambda x: x['citation_count'], reverse=True)
        for i, entry in enumerate(sorted_entries[:5], 1):
            author = entry.get('author', 'Unknown')
            year = entry.get('year', 'Unknown')
            report.append(f"   {i}. [{entry['ID']}] ({entry['citation_count']} citations)")
            report.append(f"      {author} ({year})")
        
        # 引用年份分布
        years = [int(entry['year']) for entry in cited_entries if 'year' in entry]
        if years:
            report.append(f"\n3. Publication Year Distribution:")
            year_counts = Counter(years)
            for year in sorted(year_counts.keys()):
                report.append(f"   {year}: {'*' * year_counts[year]} ({year_counts[year]})")
            
            avg_year = sum(years) / len(years)
            report.append(f"\n   Average publication year: {avg_year:.1f}")
            report.append(f"   Year range: {min(years)} - {max(years)}")
        
        # 作者统计
        authors = []
        for entry in cited_entries:
            if 'author' in entry:
                # 简单的作者分割，可能需要更复杂的解析
                entry_authors = entry['author'].split(' and ')
                authors.extend(entry_authors)
        
        if authors:
            report.append(f"\n4. Top Authors:")
            author_counts = Counter(authors)
            for author, count in author_counts.most_common(5):
                report.append(f"   - {author}: {count} references")
        
        return '\n'.join(report)


    def _save_organized_entries(self, cited_entries: List[Dict], uncited_entries: List[Dict]):

        """生成引用统计报告"""
        '''
        report = self.generate_citation_report(cited_entries)
        report_file = self.bib_file.with_name(self.bib_file.stem + '_report.txt')
        with open(report_file, 'w', encoding='utf-8') as report_f:
            report_f.write(report)
        '''

        """保存组织好的条目到bib文件"""
        writer = bibtexparser.bwriter.BibTexWriter()
        writer.indent = '  '
        writer.order_entries_by = None
                
        with open(self.bib_file, 'w', encoding='utf-8') as f:
            # 文件头部信息
            f.write("%"*80 + "\n")
            f.write("% Bibliography File\n")
            f.write("% Last Updated: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.write("% Total References: " + str(len(cited_entries) + len(uncited_entries)) + "\n")
            f.write("% - Cited: " + str(len(cited_entries)) + "\n")
            f.write("% - Uncited: " + str(len(uncited_entries)) + "\n")
            f.write("%"*80 + "\n\n")

            # 已引用条目部分
            f.write("%"*80 + "\n")
            f.write("% Cited References (sorted by first appearance)\n")
            f.write("% Format: [Citation Key] (cited X times)\n")
            f.write("% Source File: " + str(self.tex_file.name) + "\n")
            f.write("%"*80 + "\n\n")
            
            cited_entries.sort(key=lambda x: x['first_appearance'])
            
            # 修改：添加引用位置信息
            for entry in cited_entries:
                f.write(f"% Citation number: {entry['contexts'][0]['citation_number']}\n")  
                f.write(f"% Cited {entry['citation_count']} time{'s' if entry['citation_count'] > 1 else ''}\n")
                # 添加引用位置信息
                for context in entry['contexts']:
                    f.write(f"% Line {context['line_number']}: {context['context']}\n")
                    #f.write(f"% Citation number: {context['citation_number']}\n")
                f.write("%\n")  # 分隔不同引用位置
                
                entry_copy = self._remove_temp_fields(entry)
                f.write(writer._entry_to_bibtex(entry_copy) + "\n")
            
            # 未引用条目部分
            f.write("\n" + "%"*80 + "\n")
            f.write("% Uncited References\n")
            f.write("% These references are not currently cited in the document\n")
            f.write("% but are kept for potential future use\n")
            f.write("%"*80 + "\n\n")
            
            for entry in uncited_entries:
                entry_copy = self._remove_temp_fields(entry)
                f.write(writer._entry_to_bibtex(entry_copy) + "\n")


    def _remove_temp_fields(self, entry: Dict) -> Dict:
        """移除临时添加的字段"""
        entry_copy = entry.copy()
        entry_copy.pop('citation_count', None)
        entry_copy.pop('first_appearance', None)
        entry_copy.pop('contexts', None)  # 新增：移除上下文信息
        return entry_copy

    def get_citations_hash(self, citations: List[str], citation_stats: Dict) -> str:
        """计算引用列表的哈希值，包含引用次数信息"""
        citations_str = ','.join(f"{cite}:{citation_stats[cite]['count']}" 
                               for cite in sorted(citations))
        return hashlib.md5(citations_str.encode()).hexdigest()

    def has_citations_changed(self, content: str) -> bool:
        """检查引用是否发生变化"""
        current_citations, current_stats = self.get_citations_from_content(content)
        # 在哈希计算中包含引用顺序,使用有序的引用列表
        citations_str = ','.join(f"{cite}:{current_stats[cite]['count']}" for cite in current_citations)
        current_hash = hashlib.md5(citations_str.encode()).hexdigest()
        
        print(f"Current citations: {current_citations}")
        print(f"Current hash: {current_hash}")
        print(f"Last hash: {self.last_citations_hash}")
        
        if self.last_citations_hash != current_hash:
            self.last_citations_hash = current_hash
            return True
        return False

class TexChangeHandler(FileSystemEventHandler):
    def __init__(self, manager: BibReferenceManager):
        self.manager = manager
        self.last_processed_time = 0
        self.cooldown = 1
        self.last_content = None
        
    def on_modified(self, event):
        current_time = time.time()
        if (event.src_path.endswith('.tex') and 
            current_time - self.last_processed_time > self.cooldown):
            
            content = self.manager.get_tex_content()
            if content != self.last_content and self.manager.has_citations_changed(content):
                print(f"\nCitation changes detected in {event.src_path}")
                cited, uncited = self.manager.process_bib_file()
                print(f"References updated:\n- Cited: {cited}\n- Uncited: {uncited}")
            
            self.last_content = content
            self.last_processed_time = current_time

def watch_files(tex_path: str, bib_path: str):
    """监视tex文件的引用变化"""
    manager = BibReferenceManager(tex_path, bib_path)
        # 启动时先进行一次更新
    print("Initializing bibliography...")
    cited, uncited = manager.process_bib_file()
    print(f"Initial references processed:\n- Cited: {cited}\n- Uncited: {uncited}")
    print("\n" + "="*50)
    
    event_handler = TexChangeHandler(manager)
    observer = Observer()
    observer.schedule(event_handler, path=str(Path(tex_path).parent), recursive=False)
    observer.start()
    
    print(f"Watching for citation changes in {tex_path}...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file watch...")
        observer.stop()
    observer.join()

def find_tex_and_bib_files(directory: str = '.') -> Tuple[List[str], List[str]]:
    """查找目录中的 .tex 和 .bib 文件"""
    tex_files = glob.glob(f"{directory}/**/*.tex", recursive=True)
    bib_files = glob.glob(f"{directory}/**/*.bib", recursive=True)
    return tex_files, bib_files

def select_files(tex_files: List[str], bib_files: List[str]) -> Tuple[str, str]:
    """让用户选择要使用的文件"""
    if not tex_files:
        raise FileNotFoundError("No .tex files found in the current directory")
    if not bib_files:
        raise FileNotFoundError("No .bib files found in the current directory")

    print("\nFound .tex files:")
    for i, file in enumerate(tex_files, 1):
        print(f"{i}. {file}")

    print("\nFound .bib files:")
    for i, file in enumerate(bib_files, 1):
        print(f"{i}. {file}")

    # 如果只有一个文件，自动选择
    selected_tex = tex_files[0] if len(tex_files) == 1 else None
    selected_bib = bib_files[0] if len(bib_files) == 1 else None

    # 如果有多个文件，让用户选择
    if not selected_tex:
        tex_choice = int(input("\nSelect tex file number: ")) - 1
        selected_tex = tex_files[tex_choice]
    
    if not selected_bib:
        bib_choice = int(input("Select bib file number: ")) - 1
        selected_bib = bib_files[bib_choice]

    return selected_tex, selected_bib

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Manage LaTeX bibliography references')
    parser.add_argument('--dir', '-d', default='.', 
                       help='Directory to search for tex and bib files (default: current directory)')
    parser.add_argument('--watch', '-w', action='store_true', 
                       help='Watch for citation changes in the tex file')
    
    args = parser.parse_args()
    
    try:
        tex_files, bib_files = find_tex_and_bib_files(args.dir)
        selected_tex, selected_bib = select_files(tex_files, bib_files)
        
        print(f"\nUsing:\nTeX file: {selected_tex}\nBib file: {selected_bib}\n")
        
        if args.watch:
            watch_files(selected_tex, selected_bib)
        else:
            manager = BibReferenceManager(selected_tex, selected_bib)
            cited, uncited = manager.process_bib_file()
            print(f"References processed:\n- Cited: {cited}\n- Uncited: {uncited}")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
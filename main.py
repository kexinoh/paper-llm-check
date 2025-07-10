from pathlib import Path
import pluggy
from core.base_check import FileScanner, hookspec

def main(path: str):
    pm = pluggy.PluginManager('paper_check')
    pm.add_hookspecs(hookspec)
    pm.load_setuptools_entrypoints('paper_check')

    checks = pm.hook.register_checks()
    scanner = FileScanner(path)
    
    print('\n=== 开始论文格式检测 ===')
    for file_path in scanner.scan_files():
        print(f'\n扫描文件: {file_path}')
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                for check in checks:
                    issues = check.check_line(line.strip(), file_path)
                    if issues:
                        print(f'第{line_num}行: {check.get_report_header()}')
                        print('\n'.join(issues))

    # 扫描结束后触发插件收尾阶段
    for check in checks:
        issues = check.finalize()
        if issues:
            print(check.get_report_header())
            print('\n'.join(issues))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help='待检测文件或目录路径')
    args = parser.parse_args()
    main(args.path)
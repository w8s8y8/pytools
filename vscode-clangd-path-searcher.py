import pathlib

if __name__ == '__main__':
    hs = set('')
    for h in pathlib.Path('.').rglob('*.h'):
        if h.is_file():
            dirs = list(h.parts)
            dirs.pop()
            hs.add('${workspaceFolder}/' + '/'.join(dirs) + '/')
    hs = list(hs)
    hs.sort()
    hs = [f'    "-I{h}",\n' for h in hs]
    hs[-1] = hs[-1].replace(',', '')

    hs.insert(0, '    "-ID:/0/AT32IDE/platform/tools/gcc-arm-none-eabi-10.3-2021.10/arm-none-eabi/include",\n')
    hs.insert(0, '{\n  "clangd.fallbackFlags": [\n')
    hs.append('  ]\n}\n')

    with open('settings.json', 'w') as fp:
        [fp.writelines(h) for h in hs]

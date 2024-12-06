import copy
import json
import os
import re


# --------------------
class App:
    # --------------------
    def __init__(self):
        self._boards_txt = '/usr/share/arduino/hardware/arduino/avr/boards.txt'
        self._boards_json = os.path.join('pyalamake', 'lib', 'boards.json')

        self._name = ''
        self._subtypename = ''
        self._info = {}
        self._in_subtype = False
        self._common_info = {}
        self._rawlines = []

        self._all_info = {}
        self._rc = 0

    # --------------------
    def run(self):
        with open(self._boards_txt, 'r', encoding='utf-8') as fp:
            lineno = 0
            while True:
                line = fp.readline()
                if not line:
                    break
                lineno += 1
                self._parse(lineno, line.strip())

            # handle last board's info
            self._handle_info(lineno)

        print('')
        print('---- generating boards.json')
        with open(self._boards_json, 'w', encoding='utf-8') as fp:
            json.dump(self._all_info, fp, indent=4)

        if self._rc > 0:
            print(f'WARN check output for errors and warnings: rc:{self._rc}')
        else:
            print(f'OK   generated info: rc:{self._rc} json: {self._boards_json}')

    # --------------------
    def _parse(self, lineno, line):
        if line.startswith('#'):
            # skip comments
            return

        if line == '':
            # skip empty lines
            return

        m = re.search(r'(.*)=(.*)', line)
        if not m:
            self._rc += 1
            print(f'ERR  {lineno: >4}: no equals: {line}')
            return

        arg = m.group(1)
        value = m.group(2)
        if arg == 'menu.cpu':
            # ignore line
            return

        m = re.search(r'([^.]+)\.(.*)', arg)
        if not m:
            self._rc += 1
            print(f'ERR  {lineno: >4}: invalid arg: {line}')
            return
        name = m.group(1)
        arg2 = m.group(2)

        if name != self._name:
            self._handle_info(lineno)
            self._subtypename = ''
            self._handle_new_processor(lineno, name)
            self._name = name
            self._common_info = {}

        if arg2.startswith('menu.cpu'):
            # print(f'DBG  {lineno: >4}: subtype: {line}')
            self._in_subtype = True
            m = re.search(r'menu\.cpu\.([^.]+)', arg2)
            if not m:
                self._rc += 1
                print(f'ERR  {lineno: >4}: m is none, subtype: {line}')
            else:
                subtypename = m.group(1)
                if subtypename != self._subtypename:
                    if self._subtypename != '':
                        self._handle_info(lineno)

                    self._subtypename = subtypename
                    self._rawlines = []
                    print(f'\n==== {lineno: >4}: {self._name}-{self._subtypename}')

                    if self._common_info == {}:
                        self._common_info = copy.deepcopy(self._info)
                    self._info['name'] = f'{self._name}-{self._subtypename}'
                    self._info['fullname'] = f'{self._common_info["fullname"]} - {value}'
            arg2 = arg2.replace(f'menu.cpu.{self._subtypename}.', '')
        else:
            self._in_subtype = False

        self._rawlines.append(line)
        if arg2 == 'name':
            self._info['fullname'] = value
        elif arg2 == 'upload.tool':
            self._info['upload.tool'] = value
        elif arg2 == 'upload.speed':
            self._info['upload.speed'] = value
        elif arg2 == 'upload.protocol':
            self._info['upload.protocol'] = value
        elif arg2 == 'build.mcu':
            self._info['build.mcu'] = value
        elif arg2 == 'build.f_cpu':
            self._info['build.f_cpu'] = value.replace('L', '')
        elif arg2 == 'build.board':
            self._info['build.board'] = value
        elif arg2 == 'build.core':
            self._info['build.core'] = value
        elif arg2 == 'build.variant':
            self._info['build.variant'] = value

    # --------------------
    def _handle_new_processor(self, lineno, name):
        self._rawlines = []
        self._info = {
            'name': name,
            'fullname': 'unknown',
            'upload.tool': 'unknown',
            'upload.speed': 'unknown',
            'build.mcu': 'unknown',
            'build.f_cpu': 'unknown',
            'build.board': 'unknown',
            'build.core': 'unknown',
            'build.variant': 'unknown',
        }
        print(f'\n==== {lineno: >4}: {name}')

    # --------------------
    def _handle_info(self, lineno):
        if self._info == {}:
            # nothing to do; no error
            return

        print(f'INFO {lineno: >4}: {self._info}')

        # check if any unknowns, if so, print lines
        if self._name == 'gemma':
            # Note: so far, gemma is the only one with an "unknown"
            print(f'     {lineno: >4}: note: gemma does not use UART to upload')
        elif 'unknown' in self._info.values():
            self._rc += 1
            print(f'WARN {lineno: >4}: info has "unknown" values')
            # for line in self._rawlines:
            #     print(f'DBG  -- {line}')

        self._all_info[self._info['name'].lower()] = copy.deepcopy(self._info)


# --------------------
def main():
    app = App()
    app.run()


main()

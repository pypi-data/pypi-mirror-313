import sys
import traceback
import wx.py.dispatcher as dp
from .utility import get_tree_item_path, get_tree_item_name

class Convert:
    def __init__(self):
        self.label = ''
        self.equation = ''
        self.inputs = []
        self.args = []
        self.outputs = []
        self.options = {'force_select_signal': False}
    
    def GetSetting(self):
        return {'label': self.label, 'inputs': self.inputs,
                'outputs': self.outputs, 'equation': self.equation,
                'args': self.args, 'options': self.options}

    def SetSetting(self, settings):
        self.Label(settings.get('label', self.label)) \
            .Equation(settings.get('equation', self.equation)) \
            .Inputs(settings.get('inputs', self.inputs)) \
            .Outputs(settings.get('outputs', self.outputs)) \
            .Arguments(settings.get('args', self.args)) \
            .Options(settings.get('options', {})) 

    def Label(self, label):
        self.label = label
        return self
    
    def Equation(self, equation):
        self.equation = equation
        return self
    
    def Inputs(self, inputs):
        self.inputs = inputs
        return self
    
    def Outputs(self, outputs):
        self.outputs = outputs
        return self
    
    def Arguments(self, args):
        self.args = args
        return self

    def Options(self, options):
        self.Options.update(options)

    def doConvert(self, inputs, tree):
        # calculate equation(inputs)
        # inputs is the dict, e.g., {'#w', 'vehicle_attitude.q[0]'}
        # and equation may look like foo(#1, #2, #3, ...), e.g., where #1 will
        # be replaced with data from paths[0], etc.
        data = {}
        equation = self.equation
        for k, v in inputs.items():
            d = tree.GetItemDataFromPath(get_tree_item_path(v))
            if d is None:
                print(f'Invalid inputs {v}')
                return None
            data[k] = d
            equation = equation.replace(k, f'data[{k}]')

        # or '#' for first input
        #equation = equation.replace('#', 'data[0]')

        # arguments
        args = self.args
        if args is None:
            args = []
        for _, arg, value in args:
            equation = equation.replace(arg, str(value))

        try:
            # get the locals from shell, to reuse the functions/modules
            resp = dp.send('shell.get_locals')
            if resp:
                local = resp[0][1]
                local.update(locals())
            else:
                local = locals()
            d = eval(equation, globals(), local)
            return d
        except:
            traceback.print_exc(file=sys.stdout)

        return None

    def Convert(self, inputs, tree):
        # inputs is the dict, e.g., {'#w', 'vehicle_attitude.q[0]'}
        d = self.doConvert(inputs, tree)
        
        if len(self.outputs) == 1:
            d = [d]
        
        rst = []
        for output in self.outputs:
            if output == '_':
                # ignore place holder
                continue
            for i in inputs:
                # replace the name place holder in output, e.g., for ~#1
                # '#1' will be replace with the actual signal for '#1'
                output = output.replace(i, get_tree_item_path(inputs[i])[-1])
            rst.append([output, d[0]])
        
        return rst


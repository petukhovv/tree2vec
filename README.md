# ast2vec

### Description

Transformation AST of some programming language code to a vector.
The vector is constructed using feature extraction from AST.

Program consist the following feature extractors:
- **DepthExtractor** - min, max or mean depth extraction from AST;
- **CharsLengthExtractor** - min, max or mean chars length (for some node) from AST;
- **NGramsNumberExtractor** - calculating number of specified n-grams.

### AST format

The program is required on input the AST of the following format (example input):
```
[
   {
      "type":"FUN",
      "chars":"override fun onCreateView(inflater: LayoutInflater?, container: ViewGroup?, savedInstanceState: Bundle?): View? {\n        dialog.window.requestFeature(Window.FEATURE_NO_TITLE)\n\n        DaggerAppComponent.builder()\n                .appModule(AppModule(context))\n                .mainModule((activity.application as MyApplication).mainModule)\n                .build().inject(this)\n\n        var view = inflater?.inflate(R.layout.dialog_signup, container, false)\n\n        ButterKnife.bind(this, view!!)\n\n        return view\n    }",
      "children":[
         {
            "type":"MODIFIER_LIST",
            "chars":"override",
            "children":[
               {
                  "type":"override",
                  "chars":"override"
               }
            ]
         },
         {
            "type":"IDENTIFIER",
            "chars":"onCreateView"
         },
         {
            "type":"VALUE_PARAMETER_LIST",
            "chars":"(inflater: LayoutInflater?, container: ViewGroup?, savedInstanceState: Bundle?)",
            "children":[
               {
                  "type":"LPAR",
                  "chars":"("
               },
               {
                  "type":"VALUE_PARAMETER",
                  "chars":"inflater: LayoutInflater?",
                  "children":[
                     {
                        "type":"IDENTIFIER",
                        "chars":"inflater"
                     }
                  ]
               }
            ]
         }
      ]
   }
]
```
It is Kotlin AST, generated [**Kotlin custom compiler**](https://github.com/PetukhovVictor/kotlin-academic/tree/vp/ast_printing_text)

Also reqired AST transformer, which is a part of [**github-kotlin-code-collector**](https://github.com/PetukhovVictor/github-kotlin-code-collector) (see `src/lib/helper/AstHelper.py`)

File with JSON representation of AST must be passed as an argument of program.

For example: `python src/main.py ast/my_program.json`

### Vector format

Program output is map with name and value features.

Feature values is vector components.

For example:
```
{
  'chars_length_avg': 47.297029702970299,
  'chars_length_max': 2047,
  'depth': 16,
  'depth_avg': 6.3469387755102042,
  'dqe_dqe_1': 0.06373937677053824,
  'dqe_dqe_2': 0.028368794326241134,
  'dqe_dqe_4': 0.005689900426742532
}
```

### Feature configuration

Features are specified in main.py (keys array for simple features; and objects array for n-grams and other (in the future)).

For example:
```
simple_features = [
    'depth',
    'depth_avg',
    'chars_length_avg',
    'chars_length_max'
]

features = [
    {
        'type': 'ngram',
        'params': {
            'name': 'dqe_dqe_1',
            'node_types': ['CALL_EXPRESSION'],
            'max_distance': 4
        }
    },
    {
        'type': 'ngram',
        'params': {
            'name': 'dqe_dqe_4',
            'node_types': ['DOT_QUALIFIED_EXPRESSION', 'REFERENCE_EXPRESSION', 'IDENTIFIER'],
            'max_distance': 1
        }
    },
    {
        'type': 'ngram',
        'params': {
            'name': 'dqe_dqe_2',
            'node_types': ['DOT_QUALIFIED_EXPRESSION', 'DOT_QUALIFIED_EXPRESSION'],
            'max_distance': 1
        }
    }
]
```
`node_types` - type of nodes, which should be on the one path in AST (according to specified distance).
`name` - name of feature, it used in output (feature names).

import sys
sys.path.append("..") # Adds location od PYcppStyleTokenizer.py to python modules path.

from PYcppStyleTokenizer import tokenize

input = '''//comment1
void functionA(int a,int b)
{
  int a1[2] = {1,0};

  int banana2[2][2] = {
   {0, 1},   /*  row 0 */
   {4, 5},   /*  row 1 */
  };

/*multi
line
 comment2*/
int c = 0;
 "this is a \\"string\\""
 {
        a = b + c *  0.05;
 }
if(a <= b) { f_do(a); }


for(int i=0;i<10;i++)
{
  print( functionA(i,i) );
}

}'''

print "== INPUT =========================================="
line=0
for lineStr in input.split("\n"):
  sys.stdout.write('%4d:%s\n' % (line,lineStr))
  line+=1

print "==================================================="

print "== OUTPUT: ========================================"
line = -1
for token in tokenize(input):

  blockSpc = '' #indentation of code block
  if token.blockDepth:
    blockSpc= ''.join([ '-' for i in range(0,token.blockDepth) ])+'>'

  argSpc = '' #indentation of arguments
  if token.argDepth:
    argSpc = ''.join([ '-' for i in range(0,token.argDepth) ])+'>'

  arrSpc = '' #indentation of array
  if token.arrDepth:
    arrSpc = '<-'+''.join([ '-' for i in range(0,token.argDepth) ])

  value=token.value.replace("\n","\\n")

  print '[%4d:%4d]:%s %10s %s %s %s' % (token.line,token.column,blockSpc,token.typ,argSpc,value,arrSpc)

print "==================================================="

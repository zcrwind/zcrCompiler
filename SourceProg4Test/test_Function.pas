program testFunc;
var i: integer;
function foo(i: integer):integer;
begin
	foo := i+1;
end;
begin
	i := foo(2);
end.
# For animathica
# Very very rudimentary ideas for a type-theory system?

class Type:
    def __new__(cls, formation, construction, elimination, uniqueness):
        if formation.parameters: #TODO: Create class for formation, constructors, etc. to be defined from so that 'parameters' is valid.
            return unformed(formation.parameters, construction, elimination, uniqueness)  #TODO: Create Unformed.
        if not construction:
            return Empty #TODO: Create `Empty`
        defined = []
        undefined = []
        for constructor in construction:
            if constructor.parameters:
                undefined.append(constructor)
                continue
            defined.append(constructor)
        
        for eliminator in eliminators:
            pass # TODO: Extract inductor and recursor cases of eliminators. (Dependant and non-dependant eliminators. 
        # I don't need to do computation, right?
        #TODO: refl/uniqueness?

# Formation: Takes type parameters and returns constructor, eliminator, and unique... wait, do I even need Type?

def main():
    # namespaces?
    # Some thinking.
    '''Nat = Form(
            (), 
            {'number'=int},   
            {
                'Zero':((),{'number'=0}), 
                'Succ':((Var('n'), {'number'=lambda n: n.number+1}))
            },
            {
                'rec': (Function[C:U](C->(Nat->C->C)->Nat->C),rec(C, c0,cs,Zero)=c0,rec(C,c0,cs,Succ(n) = cs(n,rec(C,c0,cs,n)))),
                                                                                                             'ind': (Function[C:Nat->U](C(0)->(Function[n:N](C(n)->C(Succ(n))))->Function[n:N]C(n)),ind(C,c0,cs,0) = c0, ind(C, c0, cs, Succ(n))=cs(n,ind(C,c0,cs,n)))
            }
            {
                'refl':refl
            }
        )'''

if __name__=='__main__':
    main()

APP=main.py
INPUT=sample.txt
KEY=key.txt

DEC_POSTFIX=decrypted
ENC_POSTFIX=encrypted

SUB=substitution
PER=permutation
SCA=scaling

ISUB=$(SUB)_$(ENC_POSTFIX)
IPER=$(PER)_$(ENC_POSTFIX)
ISCA=$(SCA)_$(ENC_POSTFIX)
OSUB=$(SUB)_$(DEC_POSTFIX)
OPER=$(PER)_$(DEC_POSTFIX)
OSCA=$(SCA)_$(DEC_POSTFIX)


magic: sub per sca

clear:
	rm $(ISUB) $(OSUB) $(IPER) $(OPER) $(ISCA) $(OSCA)

sub:
	./$(APP) -i $(INPUT) -o $(ISUB) --seed $(SEED) --action enc --algorithm sub
	./$(APP) -i $(ISUB)  -o $(OSUB) --seed $(SEED) --action dec --algorithm sub

per:
	./$(APP) -i $(INPUT) -o $(IPER) --seed $(SEED) --action enc --algorithm per
	./$(APP) -i $(IPER)  -o $(OPER) --seed $(SEED) --action dec --algorithm per

sca:
	./$(APP) -i $(INPUT) -o $(ISCA) --seed $(SEED) --action enc --key $(KEY) --algorithm sca
	./$(APP) -i $(ISCA)  -o $(OSCA) --seed $(SEED) --action dec --key $(KEY) --algorithm sca

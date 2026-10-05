dp1: dp1.c
	gcc -O3 -Wall -o dp1 dp1.c

run_dp1: dp1
	./dp1 1000000 1000 | tee -a dp1_result1.txt
	./dp1 300000000 20 | tee -a dp1_result1.txt
	./dp1 1000000 1000 | tee -a dp1_result2.txt
	./dp1 300000000 20 | tee -a dp1_result2.txt
	./dp1 1000000 1000 | tee -a dp1_result3.txt
	./dp1 300000000 20 | tee -a dp1_result3.txt

dp2: dp2.c
	gcc -O3 -Wall -o dp2 dp2.c

run_dp2: dp2
	./dp2 1000000 1000 | tee -a dp2_result1.txt
	./dp2 300000000 20 | tee -a dp2_result1.txt
	./dp2 1000000 1000 | tee -a dp2_result2.txt
	./dp2 300000000 20 | tee -a dp2_result2.txt
	./dp2 1000000 1000 | tee -a dp2_result3.txt
	./dp2 300000000 20 | tee -a dp2_result3.txt

dp3: dp3.c
	gcc -O3 -Wall -o dp3 dp3.c \
		-I/opt/intel/oneapi/mkl/latest/include \
		-L/opt/intel/oneapi/mkl/latest/lib -lmkl_rt \
		-Wl,-rpath,/opt/intel/oneapi/mkl/latest/lib

run_dp3: dp3
	./dp3 1000000 1000 | tee -a dp3_result1.txt
	./dp3 300000000 20 | tee -a dp3_result1.txt
	./dp3 1000000 1000 | tee -a dp3_result2.txt
	./dp3 300000000 20 | tee -a dp3_result2.txt
	./dp3 1000000 1000 | tee -a dp3_result3.txt
	./dp3 300000000 20 | tee -a dp3_result3.txt

clean:
	rm -f dp1 dp2 dp3
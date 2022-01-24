BITS 64
;; Subroutine to print an integer
;; in the rax register
_printRAX:
	mov rcx, digitSpace
	mov rbx, 10
	mov [rcx], rbx
	inc rcx
	mov [digitSpacePos], rcx

_printRAXLoop:
	mov rdx, 0
	mov rbx, 10
	div rbx
	push rax
	add rdx, 48

	mov rcx, [digitSpacePos]
	mov [rcx], dl
	inc rcx
	mov [digitSpacePos], rcx

	pop rax
	cmp rax, 0
	jne _printRAXLoop

_printRAXLoop2:
	mov rcx, [digitSpacePos]

	mov rax, 1
	mov rdi, 1
	mov rsi, rcx
	mov rdx, 1
	syscall

	mov rcx, [digitSpacePos]
	dec rcx
	mov [digitSpacePos], rcx

	cmp rcx, digitSpace
	jge _printRAXLoop2

	ret



_mod:
    add r10, 8
    pop r14
    mov [returnstack+r10], r14
_addr1:
    ;; DIVIDE ;;
    pop rbx
    pop rax
    mov rdx, 0
    idiv rbx
    push rax
    push rdx
_addr2:
    ;; swap ;;
    pop rax
    pop rbx
    push rax
    push rbx
_addr3:
    ;; POP ;;
    pop r13

_addr4:
mov r14, [returnstack+r10]
push r14
sub r10, 8
ret
_is_prime:
    add r10, 8
    pop r14
    mov [returnstack+r10], r14
_addr6:
    ;; POP:n ;;
    pop r13
    mov [memory+0], r13
_addr7:
    ;; PUSH 2 ;;
    push 2

_addr8:
    ;; POP:counter ;;
    pop r13
    mov [memory+8], r13
_addr9:
    ;; PUSH 1 ;;
    push 1

_addr10:
    ;; while ;; 
    mov rax, [rsp]
    test rax, rax
    jz _addr20
_addr11:
    ;; POP ;;
    pop r13

_addr12:
    ;; PUSH_VAR n ;;
    mov rax, [memory+0]
    push rax
_addr13:
    ;; PUSH_VAR counter ;;
    mov rax, [memory+8]
    push rax
_addr14:
call _mod
_addr15:
    ;; PUSH_VAR counter ;;
    mov rax, [memory+8]
    push rax
_addr16:
    ;; PUSH 1 ;;
    push 1

_addr17:
    ;; ADD ;;
    pop rax
    pop rbx
    add rbx, rax
    push rbx

_addr18:
    ;; POP:counter ;;
    pop r13
    mov [memory+8], r13
_addr19:
    ;; end ;;
    jmp _addr10
_addr20:
    ;; PUSH_VAR counter ;;
    mov rax, [memory+8]
    push rax
_addr21:
    ;; PUSH 1 ;;
    push 1

_addr22:
    ;; SUB ;;
    pop rax
    pop rbx
    sub rbx, rax
    push rbx

_addr23:
    ;; PUSH_VAR n ;;
    mov rax, [memory+0]
    push rax
_addr24:
    ;; = ;;
    pop rax
    pop rbx
    cmp rbx, rax
    mov rbx, 1
    mov rdx, 0
    cmove rdx, rbx
    push rdx
_addr25:
    ;; swap ;;
    pop rax
    pop rbx
    push rax
    push rbx
_addr26:
    ;; POP ;;
    pop r13

_addr27:
mov r14, [returnstack+r10]
push r14
sub r10, 8
ret
section .bss
    digitSpace resb 100
    digitSpacePos resb 8
    memory resb 800

    returnstack resb 800

section .text
    global _start:

_start:
    mov r10, -1
_addr0:
_addr5:
_addr28:
    ;; PUSH 2 ;;
    push 2

_addr29:
    pop rax
    push rax
    push rax
_addr30:
    ;; while ;; 
    mov rax, [rsp]
    test rax, rax
    jz _addr44
_addr31:
    ;; POP ;;
    pop r13

_addr32:
    pop rax
    push rax
    push rax
_addr33:
call _is_prime
_addr34:
    ;; if ;;
    pop rax
    test rax, rax
   jz _addr38
_addr35:
    pop rax
    push rax
    push rax
_addr36:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr37:
    ;; end ;;
_addr38:
    ;; PUSH 1 ;;
    push 1

_addr39:
    ;; ADD ;;
    pop rax
    pop rbx
    add rbx, rax
    push rbx

_addr40:
    pop rax
    push rax
    push rax
_addr41:
    ;; PUSH 1000 ;;
    push 1000

_addr42:
    ;; <= ;;
    pop rax
    pop rbx
    cmp rbx, rax
    mov rbx, 1
    mov rdx, 0
    cmovle rdx, rbx
    push rdx
_addr43:
    ;; end ;;
    jmp _addr30
_addr44:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall

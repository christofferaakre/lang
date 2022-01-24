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
    ;; PUSH 13 ;;
    push 13

_addr1:
    ;; PUSH 12 ;;
    push 12

_addr2:
    ;; = ;;
    pop rax
    pop rbx
    cmp rbx, rax
    mov rbx, 1
    mov rdx, 0
    cmove rdx, rbx
    push rdx
_addr3:
    ;; NOT ;;
    pop rax
    cmp rax, 0
    je _push1_4
    _push0_4:
        push 0
        jmp _finally_4
    _push1_4:
        push 1
        jmp _finally_4
_finally_4:
_addr4:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr5:
    ;; PUSH 24 ;;
    push 24

_addr6:
    ;; PUSH 22 ;;
    push 22

_addr7:
    ;; > ;;
    pop rax
    pop rbx
    cmp rbx, rax
    mov rbx, 1
    mov rdx, 0
    cmovg rdx, rbx
    push rdx
_addr8:
    ;; NOT ;;
    pop rax
    cmp rax, 0
    je _push1_9
    _push0_9:
        push 0
        jmp _finally_9
    _push1_9:
        push 1
        jmp _finally_9
_finally_9:
_addr9:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr10:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall

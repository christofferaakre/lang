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

section .text
    global _start:

_start:
_addr0:
    ;; PUSH 1 ;;
    push 1

_addr1:
    ;; while ;; 
    mov rax, [rsp]
    test rax, rax
    jz _addr13
_addr2:
    ;; swap ;;
    pop rax
    pop rbx
    push rax
    push rbx
_addr3:
    ;; PUSH 2 ;;
    push 2

_addr4:
    ;; ADD ;;
    pop rax
    pop rbx
    add rbx, rax
    push rbx

_addr5:
    pop rax
    push rax
    push rax
_addr6:
    ;; PUSH 1 ;;
    push 1

_addr7:
    ;; SUB ;;
    pop rax
    pop rbx
    sub rbx, rax
    push rbx

_addr8:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr9:
    pop rax
    push rax
    push rax
_addr10:
    ;; PUSH 1000 ;;
    push 1000

_addr11:
    ;; < ;;
    pop rax
    pop rbx
    cmp rbx, rax
    mov rbx, 1
    mov rdx, 0
    cmovl rdx, rbx
    push rdx
_addr12:
    ;; end ;;
    jmp _addr1
_addr13:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall

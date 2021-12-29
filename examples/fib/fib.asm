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
    ;; PUSH 1 ;;
    push 1

_addr2:
    ;; while ;; 
    mov rax, [rsp]
    test rax, rax
    jz _addr15
_addr3:
    pop rax
    push rax
    push rax
_addr4:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr5:
    ;; swap ;;
    pop rax
    pop rbx
    push rax
    push rbx
_addr6:
    mov rax, [rsp+8]
    push rax
_addr7:
    ;; ADD ;;
    pop rax
    pop rbx
    add rbx, rax
    push rbx

_addr8:
    pop rax
    push rax
    push rax
_addr9:
    ;; PUSH 1000 ;;
    push 1000

_addr10:
    ;; >= ;;
    pop rax
    pop rbx
    cmp rbx, rax
    mov rbx, 1
    mov rdx, 0
    cmovge rdx, rbx
    push rdx
_addr11:
    ;; if ;;
    pop rax
    test rax, rax
   jz _addr14
_addr12:
    ;; PUSH 0 ;;
    push 0

_addr13:
    ;; end ;;
_addr14:
    ;; end ;;
    jmp _addr2
_addr15:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall

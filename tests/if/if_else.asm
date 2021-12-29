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
    ;; PUSH 0 ;;
    push 0

_addr1:
    ;; if ;;
    mov rax, [rsp]
    test rax, rax
   jz _addr5
_addr2:
    ;; PUSH 100 ;;
    push 100

_addr3:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr4:
    ;; else ;; 
    jmp _addr8
_addr5:
    ;; PUSH 200 ;;
    push 200

_addr6:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr7:
    ;; end ;;
_addr8:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall

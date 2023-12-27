#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define None -32000

typedef struct page {
  int *keys;
  int nKeys;
  struct page *next;
  struct page *previous;
} page;

typedef struct list {
  struct page *head;
} list;

typedef struct linearHashing {
  list **lists;
  int m;
  float alpha_max;
  float alpha_min;
  int page_size;
  int N;
  int l;
  int nKeys;
  int nPages;
} linearHashing;

typedef struct searchResponse {
  int nAccess;
  int found;
} searchResponse;

list *NewList() {
  list *unit = (list *)malloc(sizeof(list));
  unit->head = NULL;
  return unit;
}

page *Newpage(int size) {
  page *element = (page *)malloc(sizeof(page));
  element->keys = (int *)malloc(size * sizeof(int));
  for (int i = 0; i < size; i++) {
    element->keys[i] = None;
  }
  element->nKeys = 0;
  element->next = NULL;
  element->previous = NULL;
  return element;
}

void InsertInPage(linearHashing *unit, page *element, int page_size, int key) {
  if (element->nKeys < page_size) {
    int *aux = element->keys;
    for (int i = 0; i < page_size; i++) {
      if (aux[i] == None) {
        aux[i] = key;
        break;
      }
    }
    unit->nKeys += 1;
    element->nKeys += 1;
  } else {
    if (element->next != NULL) {
      InsertInPage(unit, element->next, page_size, key);
    } else {
      page *page = Newpage(page_size);
      unit->nPages += 1;
      page->keys[0] = key;
      page->nKeys += 1;
      unit->nKeys += 1;
      element->next = page;
      page->previous = element;
    }
  }
}

void RemoveInPage(linearHashing *unit, page *element, int page_size, int key) {
  for (int i = 0; i < page_size; i++) {
    if (element->keys[i] == key) {
      element->keys[i] = None;
      element->nKeys -= 1;
      unit->nKeys -= 1;
      break;
    }
  }
}

void Append(list *unit, page *element) {
  if (unit->head == NULL) {
    unit->head = element;
  } else {
    page *aux = unit->head;
    while (aux->next != NULL)
      aux = aux->next;
    aux->next = element;
    element->previous = aux;
  }
}

// Main Function
linearHashing *NewlinearHashing(int m, float alpha_max, float alpha_min,
                                int page_size) {
  linearHashing *unit = (linearHashing *)malloc(sizeof(linearHashing));
  unit->lists = (list **)malloc(m * sizeof(list *));
  unit->m = m;
  unit->alpha_max = alpha_max;
  unit->alpha_min = alpha_min;
  unit->page_size = page_size;
  unit->N = 0;
  unit->l = 0;
  unit->nKeys = 0;
  unit->nPages = m;
  for (int i = 0; i < m; i++) {
    unit->lists[i] = NewList();
    page *page = Newpage(page_size);
    Append(unit->lists[i], page);
  }
  return unit;
}

int h(int l, int m, int key) {
  int result = key % ((1 << l) * m);
  return result;
}

void Readjust(linearHashing *unit, list *comp, page *element) {
  int *aux = element->keys;
  int valid = 0;
  for (int i = 0; i < unit->page_size; i++) {
    if (aux[i] != None) {
      valid = 1;
      break;
    }
  }
  if (valid)
    return;
  if (comp->head == element) {
    if (element->next != NULL) {
      comp->head = element->next;
      unit->nPages--;
      free(element->keys);
      free(element);
    }
  } else {
    element->previous->next = element->next;
    if (element->next != NULL)
      element->next->previous = element->previous;
    unit->nPages--;
    free(element->keys);
    free(element);
  }
}

void Insert(linearHashing *unit, int key) {
  int l = unit->l;
  int N = unit->N;
  int m = unit->m;
  int i = h(l, m, key);
  int page_size = unit->page_size;
  if (i < N)
    i = h(l + 1, m, key);
  InsertInPage(unit, unit->lists[i]->head, page_size, key);
  float alpha = (float)unit->nKeys / (unit->nPages * page_size);
  while (alpha > unit->alpha_max) {
    int list_i = (1 << l) * m + N;
    unit->lists =
        (list **)realloc(unit->lists, ((list_i + 1) * sizeof(list *)));
    unit->lists[list_i] = NewList();
    page *new_page = Newpage(page_size);
    Append(unit->lists[list_i], new_page);
    unit->nPages += 1;
    page *aux = unit->lists[N]->head;
    while (aux != NULL) {
      list *comp = unit->lists[N];
      for (int j = 0; j < page_size; j++) {
        if (aux->keys[j] == None)
          continue;
        i = h(l + 1, m, aux->keys[j]);
        if (i != N) {
          InsertInPage(unit, new_page, page_size, aux->keys[j]);
          RemoveInPage(unit, aux, page_size, aux->keys[j]);
        }
      }
      Readjust(unit, comp, aux);
      aux = aux->next;
    }
    N += 1;
    if (N >= (1 << l) * m) {
      N = 0;
      l += 1;
    }
    alpha = (float)unit->nKeys / (unit->nPages * unit->page_size);
  }
  unit->l = l;
  unit->N = N;
}

searchResponse Search(linearHashing *unit, int key) {
  int l = unit->l;
  int N = unit->N;
  int m = unit->m;
  int i = h(l, m, key);
  if (i < N)
    i = h(l + 1, m, key);
  page *aux = unit->lists[i]->head;
  searchResponse result;
  result.nAccess = 0;
  int found = 0;
  while (aux != NULL && !found) {
    result.nAccess++;
    for (int j = 0; j < unit->page_size; j++) {
      if (aux->keys[j] == key) {
        found = 1;
        break;
      }
    }
    aux = aux->next;
  }
  result.found = found;
  return result;
}

void Display(list *unit, int page_size) {
  page *aux = unit->head;
  while (aux != NULL) {
    for (int i = 0; i < page_size; i++) {
      if (aux->keys[i] != None) {
        printf("%d ", aux->keys[i]);
      }
    }
    printf("-> ");
    aux = aux->next;
  }
  printf("\n");
}

void DisplaylinearHashing(linearHashing *unit) {
  int nlists = (1 << unit->l) * unit->m + unit->N;
  for (int i = 0; i < nlists; i++) {
    Display(unit->lists[i], unit->page_size);
  }
  printf("\n");
}

int listSize(list *unit) {
  int size = 0;
  page *aux = unit->head;
  while (aux != NULL) {
    size++;
    aux = aux->next;
  }
  return size;
}

int maxListSize(linearHashing *unit) {
  int nlists = (1 << unit->l) * unit->m + unit->N;
  int max = 0;
  for (int i = 0; i < nlists; i++) {
    int size = listSize(unit->lists[i]);
    if (size > max)
      max = size;
  }
  return max;
}

void FreeList(list *unit) {
  while (unit->head != NULL) {
    page *aux = unit->head;
    free(aux->keys);
    unit->head = aux->next;
    free(aux);
  }
  free(unit);
}

void FreelinearHashing(linearHashing *unit) {
  int nlists = (1 << unit->l) * unit->m + unit->N;
  for (int i = 0; i < nlists; i++)
    FreeList(unit->lists[i]);
  free(unit->lists);
  free(unit);
}

typedef struct readResponse {
  int *vector;
  int size;
} readResponse;

readResponse readValues() {
  int max = 100;
  int *in = (int *)malloc(max * sizeof(int));
  FILE *file = fopen("stdin.txt", "r");
  if (file == NULL) {
    perror("Error");
    exit(1);
  }
  int c = 0;
  while (fscanf(file, "%d", &in[c]) != EOF)
    c++;
  fclose(file);
  readResponse result;
  result.vector = in;
  result.size = c;
  return result;
}

// A utility function to swap to integers
void swap(int *a, int *b) {
  int temp = *a;
  *a = *b;
  *b = temp;
}

// A function to generate a random permutation of arr[]
void randomize(int arr[], int n) {
  // Use a different seed value so that we don't get same
  // result each time we run this program
  srand(time(NULL));

  // Start from the last element and swap one by one. We don't
  // need to run for the first element that's why i > 0
  for (int i = n - 1; i > 0; i--) {
    // Pick a random index from 0 to i
    int j = rand() % (i + 1);

    // Swap arr[i] with the element at random index
    swap(&arr[i], &arr[j]);
  }
}

int main() {

  // Change these parameters as you wish.
  int size = 50;
  int m = 10;
  int pageSize = 4;
  double alphaMax = 0.7;
  double alphaMin = 0.5;

  int data[size];

  for (int i = 0; i < size; i++) {
    data[i] = i;
  }
  randomize(data, size);

  // Sample of basic usage.
  linearHashing *unit = NewlinearHashing(m, alphaMax, alphaMin, pageSize);

  for (int i = 0; i < size; i++) {
    Insert(unit, data[i]);
  }

  FreelinearHashing(unit);
}
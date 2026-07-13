In this notebook, we define the transitional matrix 
$$M(t)$$
of size $63\times 63$ between subjects in a given year (or decade) $t$. For example each entry $(i,j)$ is a time series, say in $t=1990$, the number of graduates in subject=j whose advisors are from subject=i. In particular, the diagonal entries are the number of students whose adisors are from the same field.

We can also normalize the matrix, so each entry becomes a probablity. There are two different ways to normalize, normalizing by row $P(t)$, and by column $Q(t)$ resepctively. More specifically, 

$$P(t)_{i,j}=\frac{M(t)_{i,j}}{\sum_jM(t)_{i,j}}$$
$$Q(t)_{i,j}=\frac{M(t)_{i,j}}{\sum_iM(t)_{i,j}}$$


For $P(t)$, each row sum to 1, while for $Q(t)$, each column sum to 1. 

The entry $P(t)\_{i,j}$ means, among all advisors in subject $i$ who produced students in $t=1990$, the proportion of students who have subject 11; While the entry $Q(t)_{i,j}$ means among all students in subject $j$ who graduated in $t=1990$, is the proportion of those whose advisor has subject $i$. In the notation of conditional probabilities 

$P_{ij​}=P(student\  subject=j∣advisor\  subject=i).$
$Q_{ij}​=P(advisor\  subject=i∣student\  subject=j).$

For example, $P(1990)_{03,68}=34.4%$

means: among observed advisor–student edges with a mathematical logic advisor, 34.4% of the students had subject 68-Computer science.

Both $P$ and $Q$ are stocastical matrices. The matrix $P$ computes future forcasts of math subjects transitions, assuming every future generation follows the same subject-transmission law; while the matrix $Q$ computes the historical "forcasts" of math subjects transitions, assuming every past generation follows the same subject-transmission law.

For example, if $x$ is a row vector consisting of number of advisors in each subject (say in a given year), then $$xP, xP^2,...$$ predicts the number of future discribution of students in different fields.

Similarly, if $y$ is a column vector consisting of number of students in each subjects (in a given year), then $$Qy, Q^{2}y...$$ "predicts" the historical distribution of advisors in different fields.

So we can use the eigenvalues to detect the "retention rate" among all math fields. There is always an eigenvalue $\lambda_1=1$ (in fact this is only true numerically, in the decade $1950$s, this number is 0.992, this is beacuse there is a zero row, and the "leakage" rolls over among the subject transations). Then the modulus of the 2nd eigenvlaue indicates the retention rate.


Row and column normalizations are related by Bayes’ rule:

$$P(A=i|S=j)=\frac{P(S=j|A=i)P(A=i)}{P(S=j)}$$

Our goal is to understand what do these matrices say about subject transitions.

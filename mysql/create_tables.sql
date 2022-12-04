CREATE TABLE Candidate(
    candidateID INT UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    party VARCHAR(30) UNIQUE NOT NULL,

    PRIMARY KEY (candidateID)
);

CREATE TABLE UserVote(
    CPF BIGINT UNIQUE NOT NULL,
    encriptedCandidateID LONGTEXT NOT NULL,

    PRIMARY KEY (CPF)
);

CREATE TABLE UrnVote(
    candidateID INT UNIQUE NOT NULL,
    votes LONGTEXT NOT NULL,

    PRIMARY KEY (candidateID),
    FOREIGN KEY (candidateID) REFERENCES Candidate(candidateID)
)